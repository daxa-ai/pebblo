import "./polyfill.js";
import { Button, Card, Header } from "./components/index.js";
import { appRoutes } from "./routes.js";
import {
  APP_DETAILS_ROUTE,
  DASHBOARD_ROUTE,
  SAFE_RETRIEVAL_APP_ROUTE,
  SAFE_RETRIEVAL_ROUTE,
} from "./constants/routesConstant.js";
import { LeftArrowIcon } from "./icons/index.js";

export function App() {
  const UI = appRoutes();
  const button =
    window.location.pathname === APP_DETAILS_ROUTE ||
    window.location.pathname === SAFE_RETRIEVAL_APP_ROUTE
      ? Button({
          variant: "text",
          btnText: "Back",
          startIcon: LeftArrowIcon({ color: "white" }),
          href:
            window.location.pathname === SAFE_RETRIEVAL_APP_ROUTE
              ? SAFE_RETRIEVAL_ROUTE
              : DASHBOARD_ROUTE,
          color: "white",
        })
      : "";

  return /*html*/ `
       <div class="app">
          ${Header()}
          <div class="h-full flex flex-col pt-9 pb-9 pl-25 pr-25 gap-3 overflow-hidden" id="display_pane">
             ${button}
             ${Card(UI)}
          </div>
       </div>
      `;
}
