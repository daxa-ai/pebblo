const PREFIX = "/pebblo";
const SCRIPT_ELEMENT = document.getElementById("main_script");
export const PROXY = SCRIPT_ELEMENT.dataset["proxy"];
export const DASHBOARD_ROUTE = PREFIX + "/";
export const APP_DETAILS_ROUTE = PREFIX + "/app/";
export const GET_REPORT = `${PROXY}${PREFIX}/report/`;
export const NOT_FOUND_ROUTE = PREFIX + "/not-found/";
