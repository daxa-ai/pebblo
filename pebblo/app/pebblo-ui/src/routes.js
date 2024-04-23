import {
  TABS_ARR_FOR_APPLICATIONS_SAFE_LOADER,
  TABS_ARR_FOR_APPLICATIONS_SAFE_RETRIEVAL,
  TAB_PANEL_ARR_FOR_APPLICATIONS_SAFE_LOADER,
  TAB_PANEL_ARR_FOR_APPLICATIONS_SAFE_RETRIEVAL,
} from "./constants/constant.js";
import {
  APP_DETAILS_ROUTE,
  DASHBOARD_ROUTE,
  NOT_FOUND_ROUTE,
  SAFE_RETRIEVAL_APP_ROUTE,
  SAFE_RETRIEVAL_ROUTE,
} from "./constants/routesConstant.js";
import {
  AppDetailsPage,
  OverviewPage,
  PageNotFound,
  SafeRetrievalAppDetails,
} from "./pages/index.js";

export function appRoutes() {
  switch (window.location.pathname) {
    case DASHBOARD_ROUTE:
      return OverviewPage({
        tabs: TABS_ARR_FOR_APPLICATIONS_SAFE_LOADER,
        tabPanels: TAB_PANEL_ARR_FOR_APPLICATIONS_SAFE_LOADER,
      });
    case SAFE_RETRIEVAL_ROUTE:
      return OverviewPage({
        tabs: TABS_ARR_FOR_APPLICATIONS_SAFE_RETRIEVAL,
        tabPanels: TAB_PANEL_ARR_FOR_APPLICATIONS_SAFE_RETRIEVAL,
      });
    case APP_DETAILS_ROUTE:
      return AppDetailsPage();
    case SAFE_RETRIEVAL_APP_ROUTE:
      return SafeRetrievalAppDetails();
    case NOT_FOUND_ROUTE:
      return PageNotFound();
    default:
      return "Not Found";
  }
}
