document.addEventListener("DOMContentLoaded", function() {
  let sidebar = document.querySelector(".sidebar");
  let closeBtn = document.querySelector("#btn");
  let searchBtn = document.querySelector(".bx-search");

  // Check if the elements exist before attaching event listeners
  if (closeBtn) {
      closeBtn.addEventListener("click", () => {
          toggleSidebar();
          menuBtnChange(); // calling the function(optional)
      });
  }

  if (searchBtn) {
      searchBtn.addEventListener("click", () => {
          toggleSidebar();
          menuBtnChange(); // calling the function(optional)
      });
  }

  // Function to toggle sidebar
  function toggleSidebar() {
      if (sidebar) {
          sidebar.classList.toggle("open");
      }
  }

  // Function to change sidebar button(optional)
  function menuBtnChange() {
      if (closeBtn && sidebar) {
          if (sidebar.classList.contains("open")) {
              closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
          } else {
              closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
          }
      }
  }
});
