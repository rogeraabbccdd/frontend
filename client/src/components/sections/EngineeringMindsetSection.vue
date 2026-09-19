<template>
	<section id="engineering-mindset" class="section-shell bg-transparent relative overflow-hidden">

		<div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
			<!-- 大區塊標題區 (標準一級 Section 規格) -->
			<div class="section-head text-center max-w-5xl mx-auto">
				<h2 class="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-black text-white tracking-tight leading-tight text-balance">
					<span class="block lg:inline">AI 時代<span class="hidden lg:inline">，</span></span><span
						class="block mt-1 lg:mt-0 lg:inline"
						>我們培養能完成產品的人</span
					>
				</h2>
			</div>

			<div class="max-w-5xl mx-auto space-y-5 sm:space-y-6">
				<!-- 5 階段工程心智 stepper -->
				<div>
					<SegmentedNav
						v-model="active"
						:items="navItems"
						variant="step"
						accent="cyan"
						hide-on-mobile
					id-prefix="engineering-mindset"
						ariaLabel="五階段工程心智"
					/>

					<div
						id="engineering-mindset-panel"
						role="tabpanel"
						:aria-labelledby="`engineering-mindset-tab-${active}`"
						class="relative rounded-3xl px-12 pb-9 pt-5 sm:mt-5 sm:px-7 sm:pb-7 sm:pt-7 bg-gradient-to-br from-slate-900/95 via-slate-900/85 to-slate-950/95 border backdrop-blur-xl shadow-2xl shadow-slate-950/70 overflow-hidden transition-colors duration-300"
						:class="current.panelBorder"
					>
						<!-- 頂部高光流線 -->
						<div
							class="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent to-transparent pointer-events-none transition-colors duration-300"
							:class="current.topLine"
						></div>

						<StepperArrows
						v-model="active"
						:total="stages.length"
						unit-label="階段"
						:active-dot="current.dotClass"
					/>

					<Transition name="panel-swap" mode="out-in">
							<!-- 固定最小高度，避免切換階段時整區高度跳動 -->
							<div :key="current.key" class="relative z-10 min-h-[9.5rem] sm:min-h-[8rem] lg:min-h-0">
								<!-- 標頭：圖示置左，右側兩行放 STEP 與階段名稱 -->
								<div class="flex items-center gap-4 sm:gap-6 mb-4">
									<div
										class="w-14 h-14 sm:w-20 sm:h-20 shrink-0 rounded-2xl sm:rounded-3xl border flex items-center justify-center shadow-inner transition-colors duration-300"
										:class="current.iconClass"
										aria-hidden="true"
									>
										<component :is="current.icon" class="w-7 h-7 sm:w-10 sm:h-10" :class="current.labelClass" :stroke-width="1.75" />
									</div>
									<div class="min-w-0 sm:flex sm:items-baseline sm:gap-3">
										<div class="text-xl sm:text-2xl font-bold tracking-wider sm:shrink-0" :class="current.labelClass">STEP {{ active + 1 }}</div>
										<h3 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight text-pretty">
											{{ current.question }}
										</h3>
									</div>
								</div>
								<p class="text-base sm:text-lg text-slate-300 leading-relaxed text-pretty">
									{{ current.detail }}
								</p>
							</div>
						</Transition>
					</div>
				</div>

				<!-- AI 實務協同場景 (原 AI Workflow 區塊收斂合併；極矮視窗收起) -->
				<div>
					<p class="text-base font-bold text-blue-300 mb-4">課堂上的 3 個 AI 實務場景</p>

					<div class="grid grid-cols-3 gap-2.5 sm:gap-5">
						<div
							v-for="scene in aiScenes"
							:key="scene.title"
							class="p-3 sm:p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 transition-colors text-center"
							:class="scene.hoverBorder"
						>
							<!-- 放大場景圖示 -->
							<div class="flex justify-center mb-2 sm:mb-3" aria-hidden="true">
								<component :is="scene.icon" class="w-7 h-7 sm:w-10 sm:h-10" :class="scene.iconClass" :stroke-width="1.75" />
							</div>
							<h3 class="text-sm sm:text-lg font-bold text-white tracking-tight sm:mb-1.5">{{ scene.title }}</h3>
							<!-- 場景說明：手機收起，桌機保留 -->
							<p class="hidden sm:block text-base text-slate-300 leading-relaxed text-pretty">
								{{ scene.summary }}
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Target, Puzzle, Handshake, ScanSearch, Rocket, Lightbulb, Search, ShieldCheck } from 'lucide-vue-next'
import SegmentedNav, { type SegmentedNavItem, type AccentName } from '@/components/common/SegmentedNav.vue'
import StepperArrows from '@/components/common/StepperArrows.vue'

// 5 階段工程心智，改以 stepper 分段呈現，一次只聚焦單一階段避免長文同屏堆疊
const stages = [
	{
		key: 'understand',
		iconClass: 'bg-cyan-500/10 border-cyan-500/30',
		labelClass: 'text-cyan-300',
		panelBorder: 'border-cyan-500/30',
		topLine: 'via-cyan-400/50',
		dotClass: 'bg-cyan-400',
		name: '理解',
		question: '需求到底是什麼？',
		detail: '先搞清楚要解決什麼問題、使用者真正想要什麼，再動手。',
		icon: Target,
	},
	{
		key: 'decompose',
		iconClass: 'bg-emerald-500/10 border-emerald-500/30',
		labelClass: 'text-emerald-300',
		panelBorder: 'border-emerald-500/30',
		topLine: 'via-emerald-400/50',
		dotClass: 'bg-emerald-400',
		name: '拆解',
		question: '這個問題怎麼拆？',
		detail: '把一個大需求切成可以各自完成的小步驟。',
		icon: Puzzle,
	},
	{
		key: 'collaborate',
		iconClass: 'bg-purple-500/10 border-purple-500/30',
		labelClass: 'text-purple-300',
		panelBorder: 'border-purple-500/30',
		topLine: 'via-purple-400/50',
		dotClass: 'bg-purple-400',
		name: '協作',
		question: '如何讓 AI 幫我加速？',
		detail: '用精準的描述請 AI 產出草稿與雛型，把時間留給判斷、設計與取捨。',
		icon: Handshake,
	},
	{
		key: 'verify',
		iconClass: 'bg-blue-500/10 border-blue-500/30',
		labelClass: 'text-blue-300',
		panelBorder: 'border-blue-500/30',
		topLine: 'via-blue-400/50',
		dotClass: 'bg-blue-400',
		name: '驗證',
		question: 'AI 做的是對的嗎？',
		detail: '逐行審閱 AI 產出的程式碼，自行除錯與測試，確認它真的符合需求。',
		icon: ScanSearch,
	},
	{
		key: 'integrate',
		iconClass: 'bg-indigo-500/10 border-indigo-500/30',
		labelClass: 'text-indigo-300',
		panelBorder: 'border-indigo-500/30',
		topLine: 'via-indigo-400/50',
		dotClass: 'bg-indigo-400',
		name: '整合',
		question: '如何真正運作？',
		detail: '串接前端、後端與資料庫並完成部署，交付一個能實際運行的完整產品。',
		icon: Rocket,
	},
]

// 各步驟的主題色：上方導覽列的作用中膠囊與下方面板共用同一個值
const STEP_ACCENTS: AccentName[] = ['cyan', 'emerald', 'purple', 'blue', 'indigo']

const active = ref(0)
const current = computed(() => stages[active.value])
const navItems = computed<SegmentedNavItem[]>(() =>
	stages.map((stage, index) => ({ key: stage.key, label: stage.name, accent: STEP_ACCENTS[index] })),
)

// AI 實務協同場景（由原 AiWorkflowSection 合併而來，統一採用精簡文案）
const aiScenes = [
	{
		icon: Lightbulb,
		title: '想法轉雛型',
		summary: '用精確 Prompt 讓 AI 快速生成版面與雛型。',
		iconClass: 'text-cyan-300',
		hoverBorder: 'hover:border-cyan-500/40',
	},
	{
		icon: Search,
		title: '報錯解讀',
		summary: '請 AI 把看不懂的報錯翻成白話並分析原因。',
		iconClass: 'text-blue-300',
		hoverBorder: 'hover:border-blue-500/40',
	},
	{
		icon: ShieldCheck,
		title: '把關驗證',
		summary: 'AI 也會犯錯，逐行審閱才能掌握主導權。',
		iconClass: 'text-emerald-300',
		hoverBorder: 'hover:border-emerald-500/40',
	},
]
</script>

