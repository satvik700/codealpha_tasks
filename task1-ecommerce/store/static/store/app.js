// Fade out flash messages and confirm quantity edits stay within limits.
document.querySelectorAll(".msg").forEach(m => setTimeout(() => m.style.display = "none", 4000));
document.querySelectorAll("input[type=number]").forEach(i => i.addEventListener("change", () => {
  const max = +i.max; if (max && +i.value > max) i.value = max;
}));
