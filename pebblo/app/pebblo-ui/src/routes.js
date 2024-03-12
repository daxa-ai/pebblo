import {
  APP_DETAILS_ROUTE,
  DASHBOARD_ROUTE,
  NOT_FOUND_ROUTE,
} from "./constants/routesConstant.js";
import { AppDetailsPage, OverviewPage, PageNotFound } from "./pages/index.js";

export function appRoutes() {
  switch (window.location.pathname) {
    case DASHBOARD_ROUTE:
      return OverviewPage();
    case APP_DETAILS_ROUTE:
      return AppDetailsPage();
    case NOT_FOUND_ROUTE:
      return PageNotFound();
    default:
      return "Not Found";
  }
}
