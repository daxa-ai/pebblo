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

export const get_Formatted_Date = (
  date,
  showTime = false,
  showTimeZone = false
) => {
  if (date) {
    const newDate = new Date(date);
    const dateOptions = { day: "2-digit", month: "short", year: "numeric" };
    if (showTime) {
      dateOptions.hour = "numeric";
      dateOptions.minute = "numeric";
    }
    if (showTimeZone) {
      dateOptions.timeZoneName = "long";
    }
    // Format the date
    const formatter = new Intl.DateTimeFormat("en-US", dateOptions);
    const formattedDate = formatter.format(newDate);
    return formattedDate;
  } else return "";
};

export const extract_Timezone = (date) => {
  const dateTimeString = date.toString();
  // Regular expression to match the timezone part
  const timezonePattern = /(?:AM|PM)\s(.+?)(?:\.|$)/;
  // Extracting the timezone using the regular expression
  const match = dateTimeString.match(timezonePattern);
  const timezone = match ? match[1] : "";
  return timezone;
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
