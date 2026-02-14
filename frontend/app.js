const workflow = ["Draft", "Review", "Approved", "Archived"];
let currentState = "Draft";

const stateElement = document.getElementById("current-state");
const auditLog = document.getElementById("audit-log");
const itemTemplate = document.getElementById("log-item-template");

function timestamp() {
  return new Date().toISOString();
}

function logEvent(message, kind = "") {
  const node = itemTemplate.content.firstElementChild.cloneNode(true);
  node.querySelector(".time").textContent = timestamp();
  const eventSpan = node.querySelector(".event");
  eventSpan.textContent = message;
  if (kind) {
    eventSpan.classList.add(kind);
  }
  auditLog.prepend(node);
}

function setState(next) {
  const currentIndex = workflow.indexOf(currentState);
  const nextIndex = workflow.indexOf(next);

  if (nextIndex === currentIndex + 1) {
    currentState = next;
    stateElement.textContent = currentState;
    logEvent(`Workflow moved to ${currentState}.`, "success");
  } else {
    logEvent(`Invalid transition from ${currentState} to ${next}.`, "warning");
  }
}

document.getElementById("document-form").addEventListener("submit", (event) => {
  event.preventDefault();

  const docId = document.getElementById("doc-id").value.trim();
  const version = document.getElementById("version").value;
  const role = document.getElementById("role").value;

  logEvent(`Draft saved for ${docId} v${version} by ${role}.`, "success");
  event.target.reset();
  document.getElementById("version").value = "1";
  document.getElementById("role").value = "Author";
});

document.querySelectorAll(".transition").forEach((button) => {
  button.addEventListener("click", () => {
    setState(button.dataset.next);
  });
});

document.getElementById("signature-form").addEventListener("submit", (event) => {
  event.preventDefault();

  const username = document.getElementById("sign-user").value.trim();
  const meaning = document.getElementById("sign-meaning").value;
  const password = document.getElementById("sign-pass").value;

  if (!username || password.length < 4) {
    logEvent("Signature failed validation. Provide username and valid password.", "warning");
    return;
  }

  logEvent(`Electronic signature applied by ${username} (${meaning}).`, "success");
  event.target.reset();
});

logEvent("UI initialized. Audit trail started.");
