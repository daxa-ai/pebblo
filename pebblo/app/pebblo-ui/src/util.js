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

export const getFormattedDate = (date) => {
  const newDate = new Date(date);
  return `${newDate.getDate()} ${
    MONTHS[newDate.getMonth()]
  } ${newDate.getFullYear()}`;
};

export const addZero = (number) => {
  if (number < 10) return `0${number}`;
  return number;
};
