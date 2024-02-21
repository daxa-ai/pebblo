import { AppDetailsPage, OverviewPage } from "./pages/index.js";

export function appRoutes() {
  switch (window.location.pathname) {
    case "/local-ui/":
      return OverviewPage();
    case "/local-ui/appDetails":
      return AppDetailsPage();
    default:
      return "Not Found";
  }
}
