// PROPS {
//   key: string,
//   value: string,
//   className: string
// }

export function KeyValue(props) {
  const { key, value, className = "" } = props;
  return /*html*/ `
      <div class="flex flex-col gap-2 inter ${className}">
         <div class="surface-60 font-12">${key}</div>
         <div class="surface-10 font-13">${value}</div>
      </div>
    `;
}
