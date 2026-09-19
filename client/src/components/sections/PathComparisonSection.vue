<template>
	<section id="path-comparison" class="section-shell bg-transparent relative overflow-hidden">

		<div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
			<!-- 區塊前導標頭 (大器單行標題，中高齡友善大字) -->
			<div class="section-head text-center max-w-4xl mx-auto">
				<h2 class="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-black text-white tracking-tight leading-tight text-balance">
					<span class="block lg:inline">不只一條路<span class="hidden lg:inline">，</span></span><span
						class="block mt-1 lg:mt-0 lg:inline"
						>該怎麼開始？</span
					>
				</h2>
				<p class="hidden sm:block text-slate-400 mt-4 text-base sm:text-lg max-w-3xl mx-auto leading-relaxed text-pretty text-center">
					三條路都有人走成，差別在你現在缺的是什麼。
				</p>
			</div>

			<div class="max-w-4xl mx-auto">
				<!-- 三種路徑分頁 -->
				<SegmentedNav
					v-model="active"
					:items="navItems"
					variant="tab"
					accent="cyan"
					id-prefix="path-comparison"
					ariaLabel="三種學習路徑比較"
				/>

				<!-- 目前路徑內容面板 -->
				<div
					id="path-comparison-panel"
					role="tabpanel"
					:aria-labelledby="`path-comparison-tab-${active}`"
					class="mt-5 sm:mt-6"
				>
					<Transition name="panel-swap" mode="out-in">
						<div
							:key="current.key"
							class="card-subsurface-glow relative rounded-3xl p-5 sm:p-7 bg-slate-900/80 backdrop-blur-xl border shadow-2xl shadow-slate-950/60 overflow-hidden"
							:class="current.panelBorder"
						>
							<!-- 標題列：放大路徑圖示，壓低整體文字比重 -->
							<div class="flex items-center gap-4 sm:gap-5 mb-4 sm:mb-5">
								<div
									class="w-14 h-14 sm:w-20 sm:h-20 shrink-0 rounded-3xl border flex items-center justify-center shadow-inner"
									:class="current.iconClass"
									aria-hidden="true"
								>
									<component :is="current.icon" class="w-7 h-7 sm:w-10 sm:h-10" :class="current.accentText" :stroke-width="1.75" />
								</div>
								<div class="min-w-0">
									<span
										v-if="current.tag"
										class="inline-block px-3 py-0.5 rounded-2xl font-bold text-sm border mb-1.5"
										:class="current.tagClass"
									>
										{{ current.tag }}
									</span>
									<h3 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
										{{ current.title }}
									</h3>
								</div>
							</div>

							<div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-5">
								<!-- 適合對象 -->
								<!-- 適合對象清單 -->
								<div class="md:col-span-2 p-4 sm:p-5 rounded-2xl bg-slate-950/70 border border-slate-800/90">
									<div class="text-base font-bold tracking-wide mb-2.5" :class="current.accentText">適合對象</div>
									<ul class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-base text-slate-300">
										<li v-for="fit in current.fits" :key="fit" class="flex items-center gap-2 whitespace-nowrap">
											<span :class="current.accentText" aria-hidden="true">•</span>
											<span>{{ fit }}</span>
										</li>
									</ul>
								</div>

								<!-- 核心優勢 -->
								<div class="space-y-1.5">
									<div class="text-lg font-black text-emerald-400 tracking-wide">核心優勢</div>
									<p class="text-base text-slate-200 leading-relaxed text-pretty">{{ current.strength }}</p>
								</div>

								<!-- 面對代價 -->
								<div class="space-y-1.5">
									<div class="text-lg font-black text-amber-400 tracking-wide">面對代價</div>
									<p class="text-base text-slate-300 leading-relaxed text-pretty">{{ current.cost }}</p>
								</div>
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
import { Laptop, School, Briefcase } from 'lucide-vue-next'
import SegmentedNav, { type SegmentedNavItem } from '@/components/common/SegmentedNav.vue'

// 3 種學習路徑，改以分頁比較呈現，一次只顯示單一路徑避免三欄長文同屏
const paths = [
	{
		key: 'self-taught',
		navLabel: '自學 + AI',
		navIcon: Laptop,
		tag: '',
		title: '自學與 AI 協作開發',
		icon: Laptop,
		fits: ['自律與執行力高', '清楚知道要學什麼', '擅長自行查資料'],
		strength: '時間自由，成本幾乎是零。',
		cost: '卡關只能自己查，容易放棄。',
		panelBorder: 'border-slate-800/90',
		iconClass: 'bg-blue-500/15 border-blue-500/40',
		tagClass: 'bg-blue-500/10 text-blue-300 border-blue-500/30',
		accentText: 'text-blue-400',
	},
	{
		key: 'training',
		navLabel: '實體職訓',
		navIcon: School,
		tag: '建議路徑',
		title: '全日制實體職訓',
		icon: School,
		fits: ['想要完整學習路徑', '卡關時需要老師', '半年能空出平日白天'],
		strength: '雙螢幕實作，老師就在現場。',
		cost: '平日白天到課，請假上限 92 小時。',
		panelBorder: 'border-cyan-500/50',
		iconClass: 'bg-cyan-500/20 border-cyan-400/50',
		tagClass: 'bg-cyan-500/20 text-cyan-300 border-cyan-400/40',
		accentText: 'text-cyan-400',
	},
	{
		key: 'on-the-job',
		navLabel: '工作中學',
		navIcon: Briefcase,
		tag: '',
		title: '在工作中邊做邊學',
		icon: Briefcase,
		fits: ['已有程式基礎', '能接觸實際專案', '可從業務中自學'],
		strength: '做的就是真實的商業需求。',
		cost: '零基礎進不去，也沒時間打底。',
		panelBorder: 'border-slate-800/90',
		iconClass: 'bg-purple-500/15 border-purple-500/40',
		tagClass: 'bg-purple-500/10 text-purple-300 border-purple-500/30',
		accentText: 'text-purple-400',
	},
]

// 預設停在「實體職訓」，維持原版高光焦點路徑
const active = ref(1)
const current = computed(() => paths[active.value])
const navItems = computed<SegmentedNavItem[]>(() =>
	paths.map((path) => ({ key: path.key, label: path.navLabel, icon: path.navIcon })),
)
</script>

