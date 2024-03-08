import { DASHBOARD_ROUTE } from "./constants/routesConstant.js";

const MONTHS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

export const get_Formatted_Date = (date) => {
  const newDate = new Date(date);
  return `${newDate.getDate()} ${MONTHS[newDate.getMonth()]
    } ${newDate.getFullYear()}`;
};

export const add_Zero = (number) => {
  if (number < 10) return `0${number}`;
  return number;
};

export const get_Text_Orientation = (align) => {
  switch (align) {
    case "start":
      return "text-start";
    case "center":
      return "text-center";
    case "end":
      return "text-end";
    default:
      return "text-start";
  }
};

export const waitForElement = (querySelector, timeout) => {
  return new Promise((resolve, reject) => {
    var timer = false;
    if (document.querySelectorAll(querySelector).length) return resolve();
    const observer = new MutationObserver(() => {
      if (document.querySelectorAll(querySelector).length) {
        observer.disconnect();
        if (timer !== false) clearTimeout(timer);
        return resolve();
      }
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
    if (timeout)
      timer = setTimeout(() => {
        observer.disconnect();
        reject();
      }, timeout);
  });
};

export const SORT_DATA = (array, order, key) => {
  if (typeof array[0][key] === "string") {
    if (order === "asc") {
      return array.sort((a, b) => a[key].localeCompare(b[key]));
    }
    return array.sort((a, b) => b[key].localeCompare(a[key]));
  }
  if (order === "asc") {
    return array.sort((a, b) => a[key] - b[key]);
  }
  return array.sort((a, b) => b[key] - a[key]);
};
