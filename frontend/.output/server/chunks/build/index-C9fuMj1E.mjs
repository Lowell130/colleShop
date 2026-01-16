import { mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderList, ssrRenderAttr, ssrInterpolate } from 'vue/server-renderer';
import { p as publicAssetsURL } from '../routes/renderer.mjs';
import { _ as _export_sfc } from './server.mjs';
import 'vue-bundle-renderer/runtime';
import '../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';
import 'unhead/server';
import 'devalue';
import 'unhead/utils';
import 'vue-router';

const _imports_0$1 = publicAssetsURL("/images/mockup_hero.png");
const _sfc_main$3 = {};
function _sfc_ssrRender$2(_ctx, _push, _parent, _attrs) {
  _push(`<section${ssrRenderAttrs(mergeProps({ class: "relative h-screen min-h-[700px] flex items-center justify-center overflow-hidden bg-slate-50" }, _attrs))}><div class="absolute inset-0 z-0"><img${ssrRenderAttr("src", _imports_0$1)} alt="Vigneto Molisano" class="w-full h-full object-cover opacity-90"></div><div class="relative z-10 text-center px-4 mt-[-10vh]"><h1 class="text-5xl md:text-7xl font-bold text-slate-800 mb-4 drop-shadow-sm"> Vini Naturali <br> del Molise </h1><p class="text-lg md:text-xl text-slate-600 mb-8 font-medium"> Dalla terra al bicchiere. Sostenibile e Autentico. </p><div class="flex justify-center gap-4"><button class="bg-green-800 text-white px-8 py-3 rounded-full hover:bg-green-900 transition shadow-lg"> Scopri i Vini </button><button class="bg-white text-green-800 border border-green-800 px-8 py-3 rounded-full hover:bg-green-50 transition shadow-lg"> La Nostra Storia </button></div></div></section>`);
}
const _sfc_setup$3 = _sfc_main$3.setup;
_sfc_main$3.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/HeroSection.vue");
  return _sfc_setup$3 ? _sfc_setup$3(props, ctx) : void 0;
};
const __nuxt_component_0 = /* @__PURE__ */ Object.assign(_export_sfc(_sfc_main$3, [["ssrRender", _sfc_ssrRender$2]]), { __name: "HeroSection" });
const _imports_0 = publicAssetsURL("/images/mockup_body.png");
const _sfc_main$2 = {};
function _sfc_ssrRender$1(_ctx, _push, _parent, _attrs) {
  _push(`<section${ssrRenderAttrs(mergeProps({ class: "py-20 px-8 bg-white overflow-hidden" }, _attrs))}><div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center"><div class="order-2 md:order-1"><h2 class="text-3xl font-serif text-green-900 mb-6">La Nostra Storia</h2><p class="text-slate-600 mb-6 leading-relaxed"> Radicati nella terra del Molise, il nostro viaggio è iniziato con una riverenza per i ritmi della natura. Ogni bottiglia racconta una storia di dedizione, sole e suolo, creata da mani che comprendono la terra. </p><p class="text-slate-600 mb-8 leading-relaxed"> Coltiviamo i nostri vitigni sulle colline di Castropignano, seguendo metodi biologici che preservano la biodiversità e garantiscono un vino puro, sincero e ricco di carattere. </p><a href="#" class="text-green-800 font-bold hover:underline decoration-2 underline-offset-4"> Leggi di più → </a></div><div class="order-1 md:order-2 relative"><div class="rounded-3xl overflow-hidden shadow-2xl rotate-2 hover:rotate-0 transition duration-500"><img${ssrRenderAttr("src", _imports_0)} alt="Mani nella terra" class="w-full h-auto object-cover"></div><div class="absolute -z-10 top-[-20px] right-[-20px] w-full h-full bg-green-100 rounded-full blur-3xl opacity-50"></div></div></div></section>`);
}
const _sfc_setup$2 = _sfc_main$2.setup;
_sfc_main$2.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/StorySection.vue");
  return _sfc_setup$2 ? _sfc_setup$2(props, ctx) : void 0;
};
const __nuxt_component_1 = /* @__PURE__ */ Object.assign(_export_sfc(_sfc_main$2, [["ssrRender", _sfc_ssrRender$1]]), { __name: "StorySection" });
const _sfc_main$1 = {
  __name: "FeaturedWines",
  __ssrInlineRender: true,
  setup(__props) {
    const wines = [
      {
        id: 1,
        name: "Verdant Reserve",
        type: "Bianco",
        price: "€25.00",
        image: "/images/mockup_hero.png"
        // Placeholder: re-using visual
      },
      {
        id: 2,
        name: "Sun-Drenched Rosé",
        type: "Rosato",
        price: "€22.00",
        image: "/images/mockup_hero.png"
      },
      {
        id: 3,
        name: "Earth & Vine",
        type: "Rosso",
        price: "€28.00",
        image: "/images/mockup_hero.png"
      }
    ];
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<section${ssrRenderAttrs(mergeProps({ class: "py-20 bg-slate-50 relative" }, _attrs))}><div class="absolute inset-0 opacity-5 pointer-events-none overflow-hidden"><svg class="absolute top-10 left-0 w-64 h-64 text-green-800" fill="currentColor" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40"></circle></svg><svg class="absolute bottom-10 right-0 w-96 h-96 text-green-800" fill="currentColor" viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80"></rect></svg></div><div class="max-w-6xl mx-auto px-8 relative z-10"><div class="text-center mb-16"><h2 class="text-3xl font-serif text-green-900 mb-4">I Nostri Vini</h2><p class="text-slate-500">Selezionati con cura dalle nostre migliori annate.</p></div><div class="grid md:grid-cols-3 gap-10"><!--[-->`);
      ssrRenderList(wines, (wine) => {
        _push(`<div class="bg-white rounded-xl p-6 shadow-sm hover:shadow-xl transition duration-300 group text-center border border-slate-100"><div class="h-64 flex items-center justify-center mb-6 relative overflow-hidden rounded-lg bg-slate-50"><img${ssrRenderAttr("src", wine.image)} class="h-full object-contain mix-blend-multiply group-hover:scale-110 transition duration-500"${ssrRenderAttr("alt", wine.name)}></div><h3 class="text-xl font-bold text-slate-800 mb-1">${ssrInterpolate(wine.name)}</h3><p class="text-sm text-green-700 font-medium uppercase tracking-wide mb-4">${ssrInterpolate(wine.type)}</p><div class="text-2xl font-serif text-slate-900 mb-6">${ssrInterpolate(wine.price)}</div><button class="w-full bg-green-800 text-white py-3 rounded-lg font-medium hover:bg-green-700 transition flex items-center justify-center gap-2"><span>Aggiungi al Carrello</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15"></path></svg></button></div>`);
      });
      _push(`<!--]--></div></div></section>`);
    };
  }
};
const _sfc_setup$1 = _sfc_main$1.setup;
_sfc_main$1.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/FeaturedWines.vue");
  return _sfc_setup$1 ? _sfc_setup$1(props, ctx) : void 0;
};
const _sfc_main = {};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs) {
  const _component_HeroSection = __nuxt_component_0;
  const _component_StorySection = __nuxt_component_1;
  const _component_FeaturedWines = _sfc_main$1;
  _push(`<main${ssrRenderAttrs(_attrs)}>`);
  _push(ssrRenderComponent(_component_HeroSection, null, null, _parent));
  _push(ssrRenderComponent(_component_StorySection, null, null, _parent));
  _push(ssrRenderComponent(_component_FeaturedWines, null, null, _parent));
  _push(`</main>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/index.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);

export { index as default };
//# sourceMappingURL=index-C9fuMj1E.mjs.map
