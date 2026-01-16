import { mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderSlot, ssrRenderList, ssrRenderAttr, ssrInterpolate } from 'vue/server-renderer';
import { _ as _export_sfc } from './server.mjs';
import '../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';
import '../routes/renderer.mjs';
import 'vue-bundle-renderer/runtime';
import 'unhead/server';
import 'devalue';
import 'unhead/utils';
import 'vue-router';

const _sfc_main$2 = {
  __name: "AppHeader",
  __ssrInlineRender: true,
  setup(__props) {
    const links = [
      { name: "I Nostri Vini", href: "#" },
      { name: "La Cantina", href: "#" },
      { name: "Sostenibilità", href: "#" },
      { name: "Contatti", href: "#" }
    ];
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<header${ssrRenderAttrs(mergeProps({ class: "absolute top-0 left-0 w-full z-50 flex justify-between items-center px-8 py-6 text-slate-800" }, _attrs))}><nav class="hidden md:flex space-x-8"><!--[-->`);
      ssrRenderList(links.slice(0, 2), (link) => {
        _push(`<a${ssrRenderAttr("href", link.href)} class="font-medium hover:text-green-700 transition">${ssrInterpolate(link.name)}</a>`);
      });
      _push(`<!--]--></nav><div class="flex flex-col items-center"><span class="text-2xl font-bold tracking-widest text-slate-900 uppercase">Terra Viva</span><span class="text-[10px] tracking-[0.2em] text-green-700 uppercase">Molise</span></div><nav class="hidden md:flex space-x-8"><!--[-->`);
      ssrRenderList(links.slice(2), (link) => {
        _push(`<a${ssrRenderAttr("href", link.href)} class="font-medium hover:text-green-700 transition">${ssrInterpolate(link.name)}</a>`);
      });
      _push(`<!--]--></nav><button class="md:hidden text-slate-900"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"></path></svg></button></header>`);
    };
  }
};
const _sfc_setup$2 = _sfc_main$2.setup;
_sfc_main$2.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/AppHeader.vue");
  return _sfc_setup$2 ? _sfc_setup$2(props, ctx) : void 0;
};
const _sfc_main$1 = {};
function _sfc_ssrRender$1(_ctx, _push, _parent, _attrs) {
  _push(`<footer${ssrRenderAttrs(mergeProps({ class: "bg-[#1a2e1a] text-white py-16 px-8 rounded-t-3xl mt-[-20px] relative z-20" }, _attrs))}><div class="max-w-6xl mx-auto grid md:grid-cols-4 gap-12"><div class="md:col-span-1"><h3 class="text-lg font-bold mb-6">Iscriviti alla Newsletter</h3><div class="flex flex-col gap-3"><input type="email" placeholder="Indirizzo email" class="bg-white/10 border border-white/20 text-white placeholder-white/50 px-4 py-3 rounded-lg focus:outline-none focus:border-green-400"><button class="bg-[#e8e6d9] text-[#1a2e1a] font-bold py-3 rounded-lg hover:bg-white transition"> Iscriviti </button></div></div><div><h4 class="font-bold mb-6 text-[#e8e6d9]">Shop</h4><ul class="space-y-3 text-sm text-gray-300"><li><a href="#" class="hover:text-white transition">Prodotti</a></li><li><a href="#" class="hover:text-white transition">Nuovi Arrivi</a></li><li><a href="#" class="hover:text-white transition">Offerte</a></li></ul></div><div><h4 class="font-bold mb-6 text-[#e8e6d9]">Azienda</h4><ul class="space-y-3 text-sm text-gray-300"><li><a href="#" class="hover:text-white transition">Chi Siamo</a></li><li><a href="#" class="hover:text-white transition">La Nostra Storia</a></li><li><a href="#" class="hover:text-white transition">Sostenibilità</a></li></ul></div><div><h4 class="font-bold mb-6 text-[#e8e6d9]">Supporto</h4><ul class="space-y-3 text-sm text-gray-300 mb-8"><li><a href="#" class="hover:text-white transition">Contatti</a></li><li><a href="#" class="hover:text-white transition">Domande Frequenti</a></li></ul><p class="text-xs text-gray-500 mt-8"> © 2026 Azienda Agricola Castropignano.<br>Tutti i diritti riservati. </p></div></div></footer>`);
}
const _sfc_setup$1 = _sfc_main$1.setup;
_sfc_main$1.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/AppFooter.vue");
  return _sfc_setup$1 ? _sfc_setup$1(props, ctx) : void 0;
};
const __nuxt_component_1 = /* @__PURE__ */ Object.assign(_export_sfc(_sfc_main$1, [["ssrRender", _sfc_ssrRender$1]]), { __name: "AppFooter" });
const _sfc_main = {};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs) {
  const _component_AppHeader = _sfc_main$2;
  const _component_AppFooter = __nuxt_component_1;
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "font-sans text-slate-900 bg-slate-50 min-h-screen flex flex-col" }, _attrs))}>`);
  _push(ssrRenderComponent(_component_AppHeader, null, null, _parent));
  _push(`<div class="flex-grow">`);
  ssrRenderSlot(_ctx.$slots, "default", {}, null, _push, _parent);
  _push(`</div>`);
  _push(ssrRenderComponent(_component_AppFooter, null, null, _parent));
  _push(`</div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("layouts/default.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const _default = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);

export { _default as default };
//# sourceMappingURL=default-fYANIIHG.mjs.map
