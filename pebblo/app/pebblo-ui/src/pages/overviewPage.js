import { Tabs } from "../components/index.js";

export function OverviewPage({ tabs, tabPanels }) {
  return /*html*/ `
       <div class="flex gap-5 flex-col h-full overflow-y-auto overflow-x-hidden">
        <div class="surface-10 inter font-14 medium">Overview</div>
         ${Tabs(tabs, tabPanels)}
       </div>
      `;
}
