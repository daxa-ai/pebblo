import { Button } from "./components/button.js";
import { Card } from "./components/card.js";
import { Header } from "./components/header.js";
import { appRoutes } from "./routes.js";

export function App() {
  const UI = appRoutes();
  return `
       <div class="app">
          ${Header()}
          <div class="h-full flex flex-col pt-9 pb-9 pl-25 pr-25 gap-3 overflow-hidden">
          ${
            window.location.pathname === "/appDetails"
              ? Button({
                  variant: "text",
                  btnText: "Back",
                  startIcon: "/static/left-arrow.png",
                  href: "/",
                  style: "color:white;",
                })
              : ""
          }
             ${Card(UI)}
          </div>
       </div>
      `;
}
