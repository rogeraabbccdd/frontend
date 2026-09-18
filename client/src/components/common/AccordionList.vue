<template>
	<div class="accordion-list space-y-3 sm:space-y-4">
		<div
			v-for="(item, index) in items"
			:key="item.key"
			class="rounded-3xl border bg-slate-900/80 backdrop-blur-xl shadow-xl shadow-slate-950/60 overflow-hidden transition-[border-color,box-shadow] duration-300"
			:class="index === modelValue ? item.activeBorder || defaultActiveBorder : 'border-slate-800/90'"
		>
			<h3>
				<button
					:id="`${idPrefix}-trigger-${index}`"
					type="button"
					:aria-expanded="index === modelValue"
					:aria-controls="`${idPrefix}-region-${index}`"
					class="accordion-trigger w-full flex items-center gap-3.5 sm:gap-5 p-3.5 sm:p-5 text-left outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-cyan-400 transition-colors duration-300 hover:bg-slate-800/40"
					@click="toggle(index)"
				>
					<!-- 放大項目圖示，壓低整體文字比重 -->
					<span
						class="accordion-icon w-14 h-14 sm:w-16 sm:h-16 shrink-0 rounded-2xl border flex items-center justify-center text-3xl sm:text-4xl shadow-inner transition-colors duration-300"
						:class="item.iconClass || defaultIconClass"
						aria-hidden="true"
					>
						<template v-if="typeof item.icon === 'string'">{{ item.icon }}</template>
						<component v-else :is="item.icon" class="w-7 h-7 sm:w-8 sm:h-8" :stroke-width="1.75" />
					</span>

					<span class="flex-grow min-w-0">
						<span
							v-if="item.eyebrow"
							class="block text-sm font-mono font-bold tracking-wider mb-0.5"
							:class="item.eyebrowClass || 'text-slate-400'"
						>
							{{ item.eyebrow }}
						</span>
						<span class="block text-lg sm:text-xl font-extrabold text-white tracking-tight text-pretty">
							{{ item.title }}
						</span>
					</span>

					<!-- 展開指示箭頭 -->
					<span
						class="shrink-0 w-8 h-8 rounded-full bg-slate-800/80 border border-slate-700/80 flex items-center justify-center text-slate-300 transition-transform duration-300"
						:class="index === modelValue ? 'rotate-180' : ''"
						aria-hidden="true"
					>
						<svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5">
							<path d="M5 8l5 5 5-5" stroke-linecap="round" stroke-linejoin="round" />
						</svg>
					</span>
				</button>
			</h3>

			<!-- 以 grid-template-rows 0fr→1fr 平滑展開，無需量測高度 -->
			<div
				:id="`${idPrefix}-region-${index}`"
				role="region"
				:aria-labelledby="`${idPrefix}-trigger-${index}`"
				class="accordion-region grid transition-[grid-template-rows] duration-300 ease-out"
				:class="index === modelValue ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
			>
				<div class="overflow-hidden">
					<div class="px-4 sm:px-5 pb-4 sm:pb-5 pl-[4.25rem] sm:pl-[5.5rem]">
						<!-- 情境引言：手機收起，桌機保留 -->
						<blockquote
							v-if="item.quote"
							class="hidden sm:block mb-3 p-4 rounded-2xl bg-slate-950/70 border border-slate-800/90 text-base text-slate-300 leading-relaxed"
						>
							{{ item.quote }}
						</blockquote>
						<p class="text-base sm:text-lg text-slate-200 leading-relaxed text-pretty">
							{{ item.body }}
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import type { Component } from 'vue'
export interface AccordionItem {
	/** 穩定識別鍵，供 v-for 綁定 */
	key: string
	/** 放大呈現的項目圖示：emoji 字串或 Lucide 元件 */
	icon: string | Component
	/** 主標題 */
	title: string
	/** 展開後的說明內文 */
	body: string
	/** 選填的標題上方小標 */
	eyebrow?: string
	/** 選填的情境引言，置於內文之前 */
	quote?: string
	/** 以下為選填的靜態色票覆寫，需為完整類名字面量供 Tailwind 掃描 */
	iconClass?: string
	eyebrowClass?: string
	activeBorder?: string
}

const props = defineProps<{
	items: AccordionItem[]
	/** 目前展開的索引，-1 代表全部收合 */
	modelValue: number
	/** 唯一 id 前綴，供 ARIA 串接 */
	idPrefix: string
}>()

const emit = defineEmits<{
	'update:modelValue': [value: number]
}>()

const defaultIconClass = 'bg-slate-800 border-slate-700/80'
const defaultActiveBorder = 'border-cyan-500/50'

// 單開式手風琴：再次點擊已展開項目即收合
function toggle(index: number) {
	emit('update:modelValue', props.modelValue === index ? -1 : index)
}
</script>

<style scoped>
@media (prefers-reduced-motion: reduce) {
	.accordion-region {
		transition: none;
	}
}
</style>
