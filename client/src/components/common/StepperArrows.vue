<template>
	<!-- 手機版階段切換控制：導覽列隱藏時，以面板兩側的左右按鈕操作 -->
	<div class="sm:hidden" aria-hidden="false">
		<button
			type="button"
			class="absolute left-1 top-1/2 -translate-y-1/2 z-20 w-11 h-11 rounded-full bg-slate-950/85 border border-slate-700/80 text-slate-200 flex items-center justify-center shadow-lg backdrop-blur-sm transition-colors active:scale-95 disabled:opacity-30 disabled:pointer-events-none"
			:aria-label="`上一個${unitLabel}`"
			:disabled="modelValue === 0"
			@click="$emit('update:modelValue', modelValue - 1)"
		>
			<svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5">
				<path d="M12 4l-6 6 6 6" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
		</button>

		<button
			type="button"
			class="absolute right-1 top-1/2 -translate-y-1/2 z-20 w-11 h-11 rounded-full bg-slate-950/85 border border-slate-700/80 text-slate-200 flex items-center justify-center shadow-lg backdrop-blur-sm transition-colors active:scale-95 disabled:opacity-30 disabled:pointer-events-none"
			:aria-label="`下一個${unitLabel}`"
			:disabled="modelValue === total - 1"
			@click="$emit('update:modelValue', modelValue + 1)"
		>
			<svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.5">
				<path d="M8 4l6 6-6 6" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
		</button>

		<!-- 進度圓點：明確告知共有幾個階段、目前在第幾個 -->
		<div class="absolute inset-x-0 bottom-3 z-20 flex items-center justify-center gap-1.5" aria-hidden="true">
			<span
				v-for="n in total"
				:key="n"
				class="h-1.5 rounded-full transition-all duration-300"
				:class="n - 1 === modelValue ? `w-5 ${activeDot}` : 'w-1.5 bg-slate-600'"
			></span>
		</div>
	</div>
</template>

<script setup lang="ts">
withDefaults(
	defineProps<{
		/** 目前索引 */
		modelValue: number
		/** 階段總數 */
		total: number
		/** 無障礙標籤用的單位名稱，例如「階段」 */
		unitLabel?: string
		/** 作用中圓點的靜態色票類名 */
		activeDot?: string
	}>(),
	{
		unitLabel: '階段',
		activeDot: 'bg-cyan-400',
	},
)

defineEmits<{
	'update:modelValue': [value: number]
}>()
</script>

<style scoped>
@media (prefers-reduced-motion: reduce) {
	button,
	span {
		transition: none !important;
	}
}
</style>
