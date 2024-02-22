import {
  APP_DETAILS_ROUTE,
  DASHBOARD_ROUTE,
} from "./constants/routesConstant.js";
import { AppDetailsPage, OverviewPage } from "./pages/index.js";

export function appRoutes() {
  switch (window.location.pathname) {
    case DASHBOARD_ROUTE:
      return OverviewPage();
    case APP_DETAILS_ROUTE:
      return AppDetailsPage();
    default:
      return "Not Found";
  }
}
