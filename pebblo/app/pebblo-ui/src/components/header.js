const MEDIA_URL = document.scripts[0].getAttribute("staticURL");

export function Header() {
  return ` <div id="header" class="relative pt-4 pb-4 pl-6 pr-6">
                <img class="cursor-pointer" src="${MEDIA_URL}/static/pebblo-icon.png" alt="Pebblo Icon" />
                <div class="mask absolute top-0 h-59 w-full left-0 -z-1"></div>
             </div>`;
}
