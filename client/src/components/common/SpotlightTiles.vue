<template>
	<div>
		<!-- 圖示磚選取列 (以放大圖示為主體，說明文字集中於下方單一面板) -->
		<div
			role="tablist"
			:aria-label="ariaLabel"
			class="grid gap-2.5 sm:gap-4"
			:class="columns"
			@keydown="onKeydown"
		>
			<button
				v-for="(item, index) in items"
				:id="`${idPrefix}-tab-${index}`"
				:key="item.key"
				ref="tabRefs"
				type="button"
				role="tab"
				:aria-selected="index === modelValue"
				:aria-controls="`${idPrefix}-panel`"
				:tabindex="index === modelValue ? 0 : -1"
				class="group flex flex-col items-center gap-2 rounded-2xl border p-3 sm:p-4 transition-all duration-300 outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950"
				:class="
					index === modelValue
						? `${item.activeTile} shadow-lg`
						: 'bg-slate-900/70 border-slate-800/90 hover:border-slate-600 hover:bg-slate-900'
				"
				@click="$emit('update:modelValue', index)"
			>
				<span
					class="leading-none transition-transform duration-300"
					:class="[
						index === modelValue ? 'scale-110' : 'group-hover:scale-105',
						typeof item.icon === 'string' ? 'text-4xl sm:text-5xl' : '',
					]"
					aria-hidden="true"
				>
					<template v-if="typeof item.icon === 'string'">{{ item.icon }}</template>
					<component
						v-else
						:is="item.icon"
						class="w-9 h-9 sm:w-11 sm:h-11"
						:class="index === modelValue ? item.iconActiveClass || 'text-cyan-300' : 'text-slate-400 group-hover:text-slate-200'"
						:stroke-width="1.75"
					/>
				</span>
				<span
					class="text-sm sm:text-base font-bold tracking-tight text-center leading-snug"
					:class="index === modelValue ? 'text-white' : 'text-slate-400'"
				>
					{{ item.navLabel }}
				</span>
			</button>
		</div>

		<!-- 目前項目詳情面板 -->
		<div
			:id="`${idPrefix}-panel`"
			role="tabpanel"
			:aria-labelledby="`${idPrefix}-tab-${modelValue}`"
			class="mt-4 sm:mt-6 rounded-3xl p-5 sm:p-8 bg-slate-900/80 backdrop-blur-xl border shadow-2xl shadow-slate-950/60 text-center"
			:class="current.panelBorder"
		>
			<Transition name="panel-swap" mode="out-in">
				<div :key="current.key">
					<div
						v-if="current.eyebrow"
						class="text-sm font-bold tracking-wider mb-1.5"
						:class="current.eyebrowClass || 'text-slate-400'"
					>
						{{ current.eyebrow }}
					</div>
					<h3
						class="text-xl sm:text-2xl font-extrabold mb-2.5 tracking-tight text-pretty"
						:class="current.titleClass || 'text-white'"
					>
						{{ current.title }}
					</h3>
					<p class="text-base sm:text-lg text-slate-300 leading-relaxed text-pretty max-w-2xl mx-auto">
						{{ current.body }}
					</p>
				</div>
			</Transition>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, ref, type Component } from 'vue'

export interface SpotlightItem {
	/** 穩定識別鍵，供 v-for 綁定 */
	key: string
	/** 磚面放大呈現的圖示：emoji 字串或 Lucide 元件 */
	icon: string | Component
	/** 選中時的 Lucide 圖示色票（完整類名字面量） */
	iconActiveClass?: string
	/** 磚面短標籤，建議 2~4 字 */
	navLabel: string
	/** 面板主標題 */
	title: string
	/** 面板說明內文 */
	body: string
	/** 選填的面板小標 */
	eyebrow?: string
	/** 選填的面板標題色票（完整類名字面量），預設純白 */
	titleClass?: string
	/** 以下為選填的靜態色票覆寫，需為完整類名字面量供 Tailwind 掃描 */
	eyebrowClass?: string
	activeTile?: string
	panelBorder?: string
}

const props = withDefaults(
	defineProps<{
		items: SpotlightItem[]
		/** 目前選取索引 */
		modelValue: number
		/** 唯一 id 前綴，供 ARIA 串接 */
		idPrefix: string
		/** 無障礙用途的選取列名稱 */
		ariaLabel: string
		/** 磚面網格欄數，需為完整類名字面量 */
		columns?: string
	}>(),
	{
		columns: 'grid-cols-2 sm:grid-cols-4',
	},
)

const emit = defineEmits<{
	'update:modelValue': [value: number]
}>()

const current = computed(() => props.items[props.modelValue] ?? props.items[0])
const tabRefs = ref<HTMLButtonElement[]>([])

// 方向鍵切換項目，符合 WAI-ARIA Tabs 自動啟動模式
function onKeydown(event: KeyboardEvent) {
	const keys = ['ArrowRight', 'ArrowLeft', 'Home', 'End']
	if (!keys.includes(event.key)) return
	event.preventDefault()
	const total = props.items.length
	let next = props.modelValue
	if (event.key === 'ArrowRight') next = (props.modelValue + 1) % total
	else if (event.key === 'ArrowLeft') next = (props.modelValue - 1 + total) % total
	else if (event.key === 'Home') next = 0
	else next = total - 1
	emit('update:modelValue', next)
	tabRefs.value[next]?.focus()
}
</script>

