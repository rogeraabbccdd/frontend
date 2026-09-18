<template>
	<div
		:id="`${idPrefix}-rail`"
		role="tablist"
		:aria-label="ariaLabel"
		class="items-stretch gap-2 sm:gap-3 flex-wrap justify-center"
		:class="[
			hideOnMobile ? 'hidden sm:flex' : 'flex',
			variant === 'step' ? 'sm:flex-nowrap sm:justify-between' : 'sm:justify-center',
		]"
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
			class="group relative flex items-center gap-2 sm:gap-2.5 rounded-2xl border px-3 py-2 sm:px-4 sm:py-3 transition-all duration-300 outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950"
			:class="[
				variant === 'step' ? 'sm:flex-1 sm:justify-center' : '',
				index === modelValue ? accentClasses.active : accentClasses.idle,
				accentClasses.ring,
			]"
			@click="select(index)"
		>
			<!-- 步驟序號或標籤圖示 -->
			<span
				v-if="variant === 'step'"
				class="flex h-7 w-7 sm:h-8 sm:w-8 shrink-0 items-center justify-center rounded-full text-base sm:text-lg font-black leading-none transition-colors duration-300"
				:class="index === modelValue ? accentClasses.markerActive : accentClasses.markerIdle"
			>
				{{ index + 1 }}
			</span>
			<span v-else-if="item.icon" class="leading-none" aria-hidden="true">
				<template v-if="typeof item.icon === 'string'">{{ item.icon }}</template>
				<component v-else :is="item.icon" class="w-5 h-5 sm:w-6 sm:h-6" :stroke-width="1.75" />
			</span>

			<span class="text-base font-bold tracking-tight whitespace-nowrap">{{ item.label }}</span>

			<!-- 分頁項目數量徽章 -->
			<span
				v-if="item.badge"
				class="rounded-full px-2 py-0.5 text-xs font-mono font-bold leading-none transition-colors duration-300"
				:class="index === modelValue ? accentClasses.markerActive : accentClasses.markerIdle"
			>
				{{ item.badge }}
			</span>
		</button>
	</div>
</template>

<script setup lang="ts">
import { computed, ref, type Component } from 'vue'

export interface SegmentedNavItem {
	/** 穩定識別鍵，供 v-for 綁定 */
	key: string
	/** 導覽列顯示文字 */
	label: string
	/** tab 樣式專用前綴圖示：emoji 字串或 Lucide 元件 */
	icon?: string | Component
	/** tab 樣式專用尾端數量徽章 */
	badge?: string
}

const props = withDefaults(
	defineProps<{
		items: SegmentedNavItem[]
		/** 目前選取索引 */
		modelValue: number
		/** step：帶序號的階段流程；tab：帶圖示的分類頁籤 */
		variant?: 'step' | 'tab'
		/** 主題色，需為下方 ACCENTS 已登錄的靜態色票，確保 Tailwind 掃描得到完整類名 */
		accent?: AccentName
		/** 無障礙用途的導覽列名稱 */
		ariaLabel: string
		/** 唯一 id 前綴，供父層面板以 `${idPrefix}-panel` 與 `${idPrefix}-tab-{n}` 完成 ARIA 串接 */
		idPrefix: string
		/** 手機隱藏整條導覽列（改由面板兩側的左右按鈕操作） */
		hideOnMobile?: boolean
	}>(),
	{
		variant: 'tab',
		accent: 'cyan',
		hideOnMobile: false,
	},
)

const emit = defineEmits<{
	'update:modelValue': [value: number]
}>()

type AccentName = 'cyan' | 'blue' | 'emerald' | 'purple' | 'amber'

// 完整靜態類名映射：Tailwind 僅掃描原始碼字面量，禁止動態拼接色票字串
const ACCENTS: Record<AccentName, { active: string; idle: string; ring: string; markerActive: string; markerIdle: string }> = {
	cyan: {
		active: 'bg-cyan-500/15 border-cyan-400/60 text-white shadow-lg shadow-cyan-950/50',
		idle: 'bg-slate-900/70 border-slate-800/90 text-slate-300 hover:border-cyan-500/40 hover:text-white',
		ring: 'focus-visible:ring-cyan-400',
		markerActive: 'bg-cyan-400 text-slate-950',
		markerIdle: 'bg-slate-800 text-slate-300 group-hover:bg-slate-700',
	},
	blue: {
		active: 'bg-blue-500/15 border-blue-400/60 text-white shadow-lg shadow-blue-950/50',
		idle: 'bg-slate-900/70 border-slate-800/90 text-slate-300 hover:border-blue-500/40 hover:text-white',
		ring: 'focus-visible:ring-blue-400',
		markerActive: 'bg-blue-400 text-slate-950',
		markerIdle: 'bg-slate-800 text-slate-300 group-hover:bg-slate-700',
	},
	emerald: {
		active: 'bg-emerald-500/15 border-emerald-400/60 text-white shadow-lg shadow-emerald-950/50',
		idle: 'bg-slate-900/70 border-slate-800/90 text-slate-300 hover:border-emerald-500/40 hover:text-white',
		ring: 'focus-visible:ring-emerald-400',
		markerActive: 'bg-emerald-400 text-slate-950',
		markerIdle: 'bg-slate-800 text-slate-300 group-hover:bg-slate-700',
	},
	purple: {
		active: 'bg-purple-500/15 border-purple-400/60 text-white shadow-lg shadow-purple-950/50',
		idle: 'bg-slate-900/70 border-slate-800/90 text-slate-300 hover:border-purple-500/40 hover:text-white',
		ring: 'focus-visible:ring-purple-400',
		markerActive: 'bg-purple-400 text-slate-950',
		markerIdle: 'bg-slate-800 text-slate-300 group-hover:bg-slate-700',
	},
	amber: {
		active: 'bg-amber-500/15 border-amber-400/60 text-white shadow-lg shadow-amber-950/50',
		idle: 'bg-slate-900/70 border-slate-800/90 text-slate-300 hover:border-amber-500/40 hover:text-white',
		ring: 'focus-visible:ring-amber-400',
		markerActive: 'bg-amber-400 text-slate-950',
		markerIdle: 'bg-slate-800 text-slate-300 group-hover:bg-slate-700',
	},
}

const accentClasses = computed(() => ACCENTS[props.accent])

const tabRefs = ref<HTMLButtonElement[]>([])

function select(index: number) {
	if (index !== props.modelValue) emit('update:modelValue', index)
}

// 將焦點移至指定索引並同步選取，符合 WAI-ARIA Tabs 自動啟動模式
function focusAt(index: number) {
	const next = (index + props.items.length) % props.items.length
	select(next)
	tabRefs.value[next]?.focus()
}

function onKeydown(event: KeyboardEvent) {
	const keys = ['ArrowRight', 'ArrowLeft', 'Home', 'End']
	if (!keys.includes(event.key)) return
	event.preventDefault()
	if (event.key === 'ArrowRight') focusAt(props.modelValue + 1)
	else if (event.key === 'ArrowLeft') focusAt(props.modelValue - 1)
	else if (event.key === 'Home') focusAt(0)
	else focusAt(props.items.length - 1)
}
</script>

<style scoped>
@media (prefers-reduced-motion: reduce) {
	button,
	span {
		transition: none !important;
	}
}
</style>
