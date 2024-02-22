import "./polyfill.js";
import { Button, Card, Header } from "./components/index.js";
import { appRoutes } from "./routes.js";
import { APP_DETAILS_ROUTE } from "./constants/constant.js";

export function App() {
  const UI = appRoutes();
  const button =
    window.location.pathname === APP_DETAILS_ROUTE
      ? Button({
          variant: "text",
          btnText: "Back",
          startIcon: "/static/left-arrow.png",
          href: "/",
          style: "color:white;",
        })
      : "";

  return /*html*/ `
       <div class="app">
          ${Header()}
          <div class="h-full flex flex-col pt-9 pb-9 pl-25 pr-25 gap-3 overflow-hidden">
             ${button}
             ${Card(UI)}
          </div>
       </div>
      `;
}
