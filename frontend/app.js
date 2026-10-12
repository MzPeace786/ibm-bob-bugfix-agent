/**
 * IBM Bob Bug-Fixing & Testing Agent - Dashboard Controller
 * Real-time WebSocket streaming, LangGraph pipeline visualization,
 * Human-in-the-Loop decision routing, and diff syntax highlighting.
 */

// DOM Elements
const wsStatus = document.getElementById('wsStatus');
const wsStatusText = document.getElementById('wsStatusText');
const engineModeText = document.getElementById('engineModeText');
const dockerToggle = document.getElementById('dockerToggle');
const dockerLabelStatus = document.getElementById('dockerLabelStatus');
const repoSelect = document.getElementById('repoSelect');
const repoTypeHelper = document.getElementById('repoTypeHelper');
const maxRetries = document.getElementById('maxRetries');
const riskThreshold = document.getElementById('riskThreshold');
const hitlToggle = document.getElementById('hitlToggle');
const startRunBtn = document.getElementById('startRunBtn');
const rollbackBtn = document.getElementById('rollbackBtn');

// Pipeline Steps
const stepTestRunner = document.getElementById('stepTestRunner');
const stepDebugger = document.getElementById('stepDebugger');
const stepApproval = document.getElementById('stepApproval');
const stepValidator = document.getElementById('stepValidator');
const statusTestRunner = document.getElementById('statusTestRunner');
const statusDebugger = document.getElementById('statusDebugger');
const statusApproval = document.getElementById('statusApproval');
const statusValidator = document.getElementById('statusValidator');

// HITL Banner
const hitlBanner = document.getElementById('hitlBanner');
const hitlRiskScore = document.getElementById('hitlRiskScore');
const hitlMessage = document.getElementById('hitlMessage');
const approvePatchBtn = document.getElementById('approvePatchBtn');
const rejectPatchBtn = document.getElementById('rejectPatchBtn');

// Metrics
const mTotalTests = document.getElementById('mTotalTests');
const mPassedTests = document.getElementById('mPassedTests');
const mFailedTests = document.getElementById('mFailedTests');
const mIteration = document.getElementById('mIteration');
const mRiskLevel = document.getElementById('mRiskLevel');

// Tabs & Content
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const diffViewer = document.getElementById('diffViewer');
const diffFileName = document.getElementById('diffFileName');
const failuresList = document.getElementById('failuresList');
const analysisText = document.getElementById('analysisText');
const anaCategory = document.getElementById('anaCategory');
const anaCommit = document.getElementById('anaCommit');
const terminalLogs = document.getElementById('terminalLogs');
const clearLogsBtn = document.getElementById('clearLogsBtn');
const historyList = document.getElementById('historyList');

// Meta
const metaActiveBranch = document.getElementById('metaActiveBranch');
const metaHeadCommit = document.getElementById('metaHeadCommit');
const metaStatus = document.getElementById('metaStatus');

// Internal App State
let activeRunId = null;
let currentPatch = null;
let socket = null;

// Initialize WebSocket
function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws`;

  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    wsStatus.querySelector('.status-dot').style.backgroundColor = 'var(--ibm-success)';
    wsStatusText.innerText = 'Connected (Live)';
    addLogLine('info', 'WebSocket telemetry stream connected to IBM Bob backend.');
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'state_update') {
        handleStateUpdate(data.state);
      }
    } catch (e) {
      // Non-JSON ping/pong
    }
  };

  socket.onclose = () => {
    wsStatus.querySelector('.status-dot').style.backgroundColor = 'var(--ibm-danger)';
    wsStatusText.innerText = 'Disconnected';
    setTimeout(connectWebSocket, 2000);
  };
}

// Handle State Updates from LangGraph
function handleStateUpdate(state) {
  if (!state) return;
  activeRunId = state.run_id;

  // 1. Update Metrics
  const tests = state.test_results || {};
  mTotalTests.innerText = tests.total_tests || 0;
  mPassedTests.innerText = tests.passed_count || 0;
  mFailedTests.innerText = tests.failed_count || 0;
  mIteration.innerText = `${state.iteration || 1} / ${state.max_retries || 3}`;

  if (state.patch_info) {
    mRiskLevel.innerText = `${state.patch_info.risk_level || 'Low'} (${state.patch_info.risk_score || 0.0})`;
    mRiskLevel.style.color = state.patch_info.risk_level === 'High' ? 'var(--ibm-danger)' :
      (state.patch_info.risk_level === 'Medium' ? 'var(--ibm-warning)' : 'var(--ibm-success)');
  }

  // 2. Update Pipeline Steps
  updatePipelineUI(state.stage, state.status);

  // 3. Update Diff & Patch
  if (state.patch_info) {
    currentPatch = state.patch_info;
    diffFileName.innerText = state.patch_info.target_file || 'target_file';
    renderUnifiedDiff(state.patch_info.patch_diff || '');

    // Root Cause Analysis Tab
    analysisText.innerText = state.patch_info.root_cause_analysis || 'No analysis recorded.';
    anaCategory.innerText = state.patch_info.bug_category || 'N/A';
    anaCommit.innerText = state.patch_info.commit_message || 'N/A';
  }

  // 4. Update Failures List
  if (tests.failures && tests.failures.length > 0) {
    renderFailures(tests.failures);
  }

  // 5. Update Logs
  if (state.logs && state.logs.length > 0) {
    renderLogs(state.logs);
  }

  // 6. Handle Human in the Loop Banner
  if (state.requires_approval && state.approved_by_human === null) {
    hitlBanner.classList.remove('hidden');
    hitlRiskScore.innerText = state.patch_info ? state.patch_info.risk_score : '0.5';
    hitlMessage.innerText = `Debugging Agent proposed a patch for '${state.patch_info?.target_file}'. Risk is ${state.patch_info?.risk_level} (${state.patch_info?.risk_score}). Manual approval required.`;
  } else {
    hitlBanner.classList.add('hidden');
  }

  // 7. Update Repo Meta
  metaActiveBranch.innerText = state.branch_name || 'main';
  metaStatus.innerText = state.status;
  if (state.status === 'SUCCESS') {
    metaStatus.className = 'tag-clean';
    loadHistory();
  }
}

// Update Pipeline Visualizer
function updatePipelineUI(stage, status) {
  // Reset classes
  [stepTestRunner, stepDebugger, stepApproval, stepValidator].forEach(s => {
    s.classList.remove('active', 'completed');
  });

  if (stage === 'TEST_RUNNER') {
    stepTestRunner.classList.add('active');
    statusTestRunner.innerText = 'Running';
  } else if (stage === 'DEBUGGING') {
    stepTestRunner.classList.add('completed');
    statusTestRunner.innerText = 'Tests Analyzed';
    stepDebugger.classList.add('active');
    statusDebugger.innerText = 'Synthesizing';
  } else if (stage === 'HUMAN_APPROVAL') {
    stepTestRunner.classList.add('completed');
    stepDebugger.classList.add('completed');
    stepApproval.classList.add('active');
    statusApproval.innerText = 'Awaiting Review';
  } else if (stage === 'VALIDATION') {
    stepTestRunner.classList.add('completed');
    stepDebugger.classList.add('completed');
    stepApproval.classList.add('completed');
    stepValidator.classList.add('active');
    statusValidator.innerText = 'Verifying';
  } else if (stage === 'COMPLETED' || status === 'SUCCESS') {
    [stepTestRunner, stepDebugger, stepApproval, stepValidator].forEach(s => {
      s.classList.add('completed');
    });
    statusValidator.innerText = 'Committed';
  }
}

// Render Diff with syntax highlighting
function renderUnifiedDiff(diffText) {
  if (!diffText || diffText.trim() === '') {
    diffViewer.innerHTML = '<code>No modifications proposed yet.</code>';
    return;
  }

  const lines = diffText.split('\n');
  const formatted = lines.map(line => {
    const escaped = escapeHtml(line);
    if (line.startsWith('+++') || line.startsWith('---') || line.startsWith('@@')) {
      return `<div class="diff-meta">${escaped}</div>`;
    } else if (line.startsWith('+')) {
      return `<div class="diff-add">${escaped}</div>`;
    } else if (line.startsWith('-')) {
      return `<div class="diff-del">${escaped}</div>`;
    }
    return `<div>${escaped}</div>`;
  }).join('');

  diffViewer.innerHTML = formatted;
}

// Render Failure Cards
function renderFailures(failures) {
  failuresList.innerHTML = failures.map(f => `
    <div class="failure-item">
      <h5>${escapeHtml(f.test_name)}</h5>
      <p><strong>Location:</strong> ${escapeHtml(f.location)} (line ${f.line})</p>
      <p><strong>Error:</strong> ${escapeHtml(f.message)}</p>
      <pre class="failure-trace">${escapeHtml(f.traceback || '')}</pre>
    </div>
  `).join('');
}

// Render Logs in Terminal
function renderLogs(logs) {
  terminalLogs.innerHTML = logs.map(l => {
    const levelClass = (l.level || 'info').toLowerCase();
    return `<div class="log-line ${levelClass}">[${l.timestamp}] [${l.stage}] ${escapeHtml(l.message)}</div>`;
  }).join('');
  terminalLogs.scrollTop = terminalLogs.scrollHeight;
}

function addLogLine(level, msg) {
  const line = document.createElement('div');
  line.className = `log-line ${level}`;
  const now = new Date().toTimeString().split(' ')[0];
  line.innerText = `[${now}] ${msg}`;
  terminalLogs.appendChild(line);
  terminalLogs.scrollTop = terminalLogs.scrollHeight;
}

function escapeHtml(str) {
  return (str || '').replace(/[&<>'"]/g, tag => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[tag] || tag));
}

// Tab Switching
tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    tabBtns.forEach(b => b.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
  });
});

// Clear Logs
clearLogsBtn.addEventListener('click', () => {
  terminalLogs.innerHTML = '';
});

// Trigger Bug-Fixing Run
startRunBtn.addEventListener('click', async () => {
  startRunBtn.disabled = true;
  startRunBtn.innerText = 'Agent Running...';
  addLogLine('agent', 'Triggering IBM Bob Automated Bug-Fixing workflow...');

  const payload = {
    repo_key: repoSelect.value,
    max_retries: parseInt(maxRetries.value, 10),
    hitl_enabled: hitlToggle.checked,
    risk_threshold: parseFloat(riskThreshold.value),
    use_docker: dockerToggle.checked
  };

  try {
    const res = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    activeRunId = data.run_id;
    addLogLine('info', `Workflow started with Run ID: ${activeRunId}`);
  } catch (err) {
    addLogLine('error', `Failed to start run: ${err.message}`);
  } finally {
    startRunBtn.disabled = false;
    startRunBtn.innerHTML = '<span class="btn-icon">▶</span> Run Bug-Fixing Agent';
  }
});

// HITL Approval Buttons
approvePatchBtn.addEventListener('click', async () => {
  if (!activeRunId) return;
  hitlBanner.classList.add('hidden');
  addLogLine('agent', 'Human reviewer approved patch. Sending validation instruction...');

  await fetch('/api/approve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ run_id: activeRunId, approved: true })
  });
});

rejectPatchBtn.addEventListener('click', async () => {
  if (!activeRunId) return;
  hitlBanner.classList.add('hidden');
  addLogLine('warning', 'Human reviewer rejected patch. Rolling back modifications...');

  await fetch('/api/approve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ run_id: activeRunId, approved: false, rejection_reason: 'Rejected by human reviewer via dashboard.' })
  });
});

// Rollback Button
rollbackBtn.addEventListener('click', async () => {
  if (confirm('Are you sure you want to rollback all working tree changes in this repository?')) {
    addLogLine('warning', 'Executing hard rollback of working tree...');
    const res = await fetch('/api/rollback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ repo_key: repoSelect.value })
    });
    const data = await res.json();
    addLogLine(data.status === 'success' ? 'success' : 'error', data.message || data.error);
    fetchDiff();
  }
});

// Repo selection helper text
repoSelect.addEventListener('change', () => {
  const isPy = repoSelect.value === 'python_calculator';
  repoTypeHelper.innerText = isPy ? 'Type: Python (pytest) | Isolated Branch: Auto-created' : 'Type: JavaScript (Jest) | Isolated Branch: Auto-created';
  fetchDiff();
});

// Fetch current Diff
async function fetchDiff() {
  try {
    const res = await fetch(`/api/diff?repo_key=${repoSelect.value}`);
    const data = await res.json();
    renderUnifiedDiff(data.diff || '');
    if (data.status) {
      metaActiveBranch.innerText = data.status.active_branch || 'main';
      metaHeadCommit.innerText = data.status.head_commit || 'HEAD';
      metaStatus.innerText = data.status.clean ? 'Clean' : 'Modified';
      metaStatus.className = data.status.clean ? 'tag-clean' : 'tag-dirty';
    }
  } catch (e) {}
}

// Fetch Fix History
async function loadHistory() {
  try {
    const res = await fetch('/api/history');
    const data = await res.json();
    if (data.history && data.history.length > 0) {
      historyList.innerHTML = data.history.map(item => `
        <div class="history-card">
          <div class="history-header">
            <span>Run #${item.run_id}</span>
            <span>${item.timestamp}</span>
          </div>
          <h5>${escapeHtml(item.bug_category)}</h5>
          <p>Fixed <code>${escapeHtml(item.target_file)}</code> in ${item.iterations} iteration(s)</p>
          <span class="history-commit">Commit: ${item.commit?.commit_short || 'N/A'}</span>
        </div>
      `).join('');
    }
  } catch (e) {}
}

// Check Backend Engine Status
async function checkEngineStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    if (data.docker_available) {
      engineModeText.innerText = 'LangGraph + Docker Engine';
      dockerLabelStatus.innerText = 'Docker Active (Container Isolation)';
      dockerToggle.disabled = false;
    } else {
      engineModeText.innerText = 'LangGraph + Isolated Sandbox';
      dockerLabelStatus.innerText = 'Isolated Sandbox (Docker Daemon Inactive)';
      dockerToggle.checked = false;
    }
  } catch (e) {}
}

// Initial Boot
window.addEventListener('DOMContentLoaded', () => {
  connectWebSocket();
  checkEngineStatus();
  fetchDiff();
  loadHistory();
});
