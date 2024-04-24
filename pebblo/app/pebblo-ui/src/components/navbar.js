export const Navbar = ({ navItems, selectedTab }) => {
  return /*html*/ `<div class="navbar">
    ${navItems.myMap(
      (tab) =>
        `<a href="${tab.link}" class="${
          selectedTab === tab.link ? "navlink-active" : ""
        }">${tab.name}</a>`
    )}
  </div>`;
};
