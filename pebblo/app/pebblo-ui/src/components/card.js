// PROPS { children: HTMLElement }
export function Card(children) {
  return /*html*/ `
      <div class="card overflow-hidden">${children}</div>
      `;
}
