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

export const getFormattedDate = (
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

export const extractTimezone = (date) => {
  const dateTimeString = date.toString();
  // Regular expression to match the timezone part
  const timezonePattern = /(?:AM|PM)\s(.+?)(?:\.|$)/;
  // Extracting the timezone using the regular expression
  const match = dateTimeString.match(timezonePattern);
  const timezone = match ? match[1] : "";
  return timezone;
};

export const addZero = (number) => {
  if (number < 10) return `0${number}`;
  return number;
};

export const getTextOrientation = (align) => {
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

export const getFileSize = (size) => {
  // Returns file size in KB, MB, GB as applicable
  if (size && size !== "-") {
    const power = 2 ** 10;
    let n = 0;
    const powerLabels = { 0: "Bytes", 1: "KB", 2: "MB", 3: "GB", 4: "TB" };
    while (size > power) {
      size /= power;
      n++;
    }
    const sizeNum = parseFloat(size.toFixed(2));
    const sizeStr = sizeNum.toString() + " " + (powerLabels[n] || "");
    return sizeStr;
  }
  return "-";
};
