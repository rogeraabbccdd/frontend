<template>
	<section id="learning-path" class="section-shell bg-transparent relative overflow-hidden">

		<div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
			<!-- 區塊標題 (大器單行標題，中高齡友善閱讀) -->
			<div class="section-head text-center max-w-4xl mx-auto">
				<h2 class="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-black text-white tracking-tight leading-tight">
					<span class="block lg:inline">從第一行程式碼<span class="hidden lg:inline">，</span></span><span
						class="block mt-1 lg:mt-0 lg:inline text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-emerald-400"
						>到自己的作品</span
					>
				</h2>
			</div>

			<div class="max-w-5xl mx-auto">
				<!-- 4 階段導覽列 -->
				<SegmentedNav
					v-model="active"
					:items="navItems"
					variant="step"
					accent="cyan"
					hide-on-mobile
					id-prefix="learning-path"
					aria-label="四階段學習歷程"
				/>

				<!-- 進度軌 (以視覺長度回饋目前走到第幾階段) -->
				<div class="hidden sm:block mt-4 h-1 w-full rounded-full bg-slate-800/80 overflow-hidden" aria-hidden="true">
					<div
						class="h-full rounded-full bg-gradient-to-r from-cyan-400 to-emerald-400 transition-[width] duration-500 ease-out"
						:style="{ width: `${((active + 1) / stages.length) * 100}%` }"
					></div>
				</div>

				<!-- 目前階段內容面板 -->
				<div
					id="learning-path-panel"
					role="tabpanel"
					:aria-labelledby="`learning-path-tab-${active}`"
					class="relative rounded-3xl px-12 pb-9 pt-5 sm:mt-5 sm:px-7 sm:pb-7 sm:pt-7 bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 shadow-2xl shadow-slate-950/60 overflow-hidden"
				>

					<StepperArrows
						v-model="active"
						:total="stages.length"
						unit-label="階段"
						active-dot="bg-cyan-400"
					/>

					<Transition name="stage-fade" mode="out-in">
							<!-- 固定最小高度，避免切換階段時整區高度跳動 -->
							<div :key="current.key" class="relative z-10 min-h-[15.5rem] sm:min-h-[13rem] lg:min-h-0">
								<!-- 標頭：圖示置左，右側兩行放 Stage 與階段名稱 -->
								<div class="flex items-center gap-4 sm:gap-6 mb-4">
									<div
										class="w-14 h-14 sm:w-20 sm:h-20 shrink-0 rounded-2xl sm:rounded-3xl border flex items-center justify-center shadow-inner"
										:class="current.iconClass"
										aria-hidden="true"
									>
										<component
											:is="current.icon"
											class="w-7 h-7 sm:w-10 sm:h-10"
											:class="current.labelClass"
											:stroke-width="1.75"
										/>
									</div>
									<div class="min-w-0 sm:flex sm:items-baseline sm:gap-3">
										<div class="text-xl sm:text-2xl font-bold tracking-wider sm:shrink-0" :class="current.labelClass">
											{{ current.stageTag }}
										</div>
										<div class="text-xl sm:text-2xl font-extrabold tracking-tight whitespace-nowrap text-white">
											{{ current.title }}
										</div>
									</div>
								</div>

								<p class="text-base sm:text-lg text-slate-300 leading-relaxed text-pretty">
									{{ current.description }}
								</p>
								<div class="mt-4 flex flex-wrap gap-2">
									<span
										v-for="skill in current.skills"
										:key="skill"
										class="px-3 py-1.5 rounded-xl bg-slate-950/70 border border-slate-800/90 text-sm font-mono font-bold"
										:class="current.labelClass"
									>
										{{ skill }}
									</span>
								</div>
							</div>
						</Transition>
				</div>
			</div>
		</div>
	</section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { LayoutTemplate, Boxes, Database, Bot } from 'lucide-vue-next'
import SegmentedNav, { type SegmentedNavItem } from '@/components/common/SegmentedNav.vue'
import StepperArrows from '@/components/common/StepperArrows.vue'

// 4 階段能力蛻變路徑，改以 stepper 分段呈現，一次只聚焦單一階段避免長文同屏堆疊
const stages = [
	{
		key: 'stage-01',
		navLabel: '看懂網頁',
		stageTag: 'STAGE 01',
		title: '看懂網頁怎麼運作',
		description: '從 HTML/CSS/JS 開始，理解畫面與互動原理，從看不懂到知道每行程式碼在做什麼。',
		icon: LayoutTemplate,
		skills: ['HTML', 'CSS', 'JavaScript'],
		iconClass: 'bg-cyan-500/10 border-cyan-500/30',
		labelClass: 'text-cyan-300',
	},
	{
		key: 'stage-02',
		navLabel: '組織系統',
		stageTag: 'STAGE 02',
		title: '學會組織前端系統',
		description: '進入 Vue 3 元件化與狀態管理，學會把功能組織成好維護的系統。',
		icon: Boxes,
		skills: ['Vue 3', '組件架構', 'Pinia'],
		iconClass: 'bg-blue-500/10 border-blue-500/30',
		labelClass: 'text-blue-300',
	},
	{
		key: 'stage-03',
		navLabel: '串接資料',
		stageTag: 'STAGE 03',
		title: '串接真實資料流',
		description: '串接 REST API 與資料庫，貫通前後端資料流，具備處理真實業務邏輯的能力。',
		icon: Database,
		skills: ['REST API', 'Node.js', '資料庫'],
		iconClass: 'bg-purple-500/10 border-purple-500/30',
		labelClass: 'text-purple-300',
	},
	{
		key: 'stage-04',
		navLabel: '協作交付',
		stageTag: 'STAGE 04',
		title: '與 AI 協作交付',
		description: '具備對 AI 提問、審核與除錯的判斷力，結合 Git 流程將 AI 轉化為真實生產力。',
		icon: Bot,
		skills: ['AI 協同', '除錯驗證', 'Git'],
		iconClass: 'bg-emerald-500/10 border-emerald-500/30',
		labelClass: 'text-emerald-300',
	},
]

const active = ref(0)
const current = computed(() => stages[active.value])
const navItems = computed<SegmentedNavItem[]>(() =>
	stages.map((stage) => ({ key: stage.key, label: stage.navLabel })),
)
</script>

<style scoped>
/* 階段切換淡入位移，維持全站 power1.out 絲滑手感 */
.stage-fade-enter-active,
.stage-fade-leave-active {
	transition: opacity 0.28s ease-out, transform 0.28s ease-out;
}

.stage-fade-enter-from {
	opacity: 0;
	transform: translateY(10px);
}

.stage-fade-leave-to {
	opacity: 0;
	transform: translateY(-6px);
}

@media (prefers-reduced-motion: reduce) {
	.stage-fade-enter-active,
	.stage-fade-leave-active {
		transition: none;
	}
}
</style>
