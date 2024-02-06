function Tabs(tabsArr, children) {
  let allTabs = "";
  let tabValue = 0;

  tabsArr?.map((tab) => (allTabs += Tab(tab)));
  document.addEventListener("DOMContentLoaded", function () {
    const tabPanel = document.getElementById("tab-panel");
    const tabElements = document.getElementsByClassName("tab");
    tabPanel.innerHTML = tabsArr[tabValue]?.tabPanel;
    Array.from(tabElements).forEach((element) => {
      element?.addEventListener("click", function (e) {
        tabValue = Number(e.target.dataset.value);
        document.getElementById("tab-selected").style.left = `${
          Number(e.target.dataset.value) * 224 +
          (Number(e.target.dataset.value)
            ? 24 * Number(e.target.dataset.value)
            : 0)
        }px`;
        tabPanel.innerHTML = "";
        tabPanel.innerHTML = tabsArr[tabValue]?.tabPanel;
      });
    });
  });

  return `
      <div class="flex flex-col">
        <div class="tabs sticky top-0 flex gap-6">
          ${allTabs}
          <div id="tab-selected"></div> 
        </div>
        <div id="tab-panel" class="h-full">${children}</div>
      </div>
      `;
}

function Tab(item) {
  return `
          <div class="tab manrope" data-value=${item?.value}>
            <div class="inline ${
              item?.isCritical ? "critical" : "surface-10"
            } font-48 font-thin pointer-none">
             ${item?.critical < 10 ? `0${item?.critical}` : item?.critical} ${
    item?.outOf
      ? `<span class="surface-10 font-24 -ml-1">/${item?.outOf}</span>`
      : ""
  }
            </div>
            <div class="font-13 inter surface-10 pointer-none">${
              item?.label
            }</div>
          </div>
         
      `;
}

export { Tabs, Tab };
