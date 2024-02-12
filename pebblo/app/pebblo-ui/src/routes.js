import { AppDetailsPage, OverviewPage } from "./pages/index.js";

export function appRoutes() {
  switch (window.location.pathname) {
    case "/":
      return OverviewPage();
    case "/appDetails":
      return AppDetailsPage();
    default:
      return "Not Found";
  }
}
