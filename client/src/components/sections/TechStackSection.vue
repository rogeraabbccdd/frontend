<template>
	<section
		id="tech-stack"
		:class="[
			hideHeader
				? 'py-6 sm:py-10 bg-transparent relative'
				: 'section-shell bg-transparent relative overflow-hidden',
		]"
	>

		<div class="max-w-[1536px] mx-auto px-4 sm:px-6 lg:px-8 2xl:px-12 relative z-10 w-full">
			<!-- 區塊標題 (僅在未隱藏標頭時渲染) -->
			<div v-if="!hideHeader" class="section-head text-center max-w-4xl mx-auto">
				<h2 class="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-black text-white tracking-tight leading-tight text-balance">
					你會接觸到哪些技術？
				</h2>
				<p
					class="hidden sm:block text-slate-400 mt-4 text-base sm:text-lg max-w-4xl mx-auto leading-relaxed text-pretty text-center"
				>
					這些都是做作品時真的會用到的工具。
				</p>
			</div>

			<div class="max-w-6xl mx-auto">
				<!-- 技術分類頁籤 (分類與數量完全由 CMS category_tab 動態推導) -->
				<SegmentedNav
					v-if="tabs.length > 1"
					v-model="active"
					:items="tabs"
					variant="tab"
					accent="cyan"
					id-prefix="tech-stack"
					ariaLabel="技術分類"
				/>

				<!-- 目前分類的技術卡片 -->
				<div
					id="tech-stack-panel"
					role="tabpanel"
					:aria-labelledby="`tech-stack-tab-${active}`"
					class="mt-5 sm:mt-6"
				>
					<Transition name="tech-fade" mode="out-in">
						<div
							:key="activeGroup.tab"
							class="grid gap-4 sm:gap-6"
							:class="gridColumns"
						>
							<div
								v-for="card in activeGroup.cards"
								:key="card.id"
								class="card-subsurface-glow relative rounded-3xl p-5 sm:p-7 bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 shadow-xl shadow-slate-950/60 overflow-hidden hover:border-cyan-500/50 transition-[border-color,box-shadow] duration-300"
							>
								<div class="flex items-start gap-4 sm:gap-5">
									<!-- 放大技術圖示，壓低整體文字比重 -->
									<div
										class="w-16 h-16 sm:w-20 sm:h-20 shrink-0 rounded-2xl bg-slate-800 border border-slate-700/80 flex items-center justify-center shadow-inner"
										aria-hidden="true"
									>
										<svg
											v-if="getTechIcon(card.tech_name).path"
											viewBox="0 0 24 24"
											class="w-8 h-8 sm:w-10 sm:h-10"
											:style="{ color: getTechIcon(card.tech_name).color }"
											fill="currentColor"
										>
											<path :d="getTechIcon(card.tech_name).path" />
										</svg>
										<component
											v-else
											:is="getTechIcon(card.tech_name).component"
											class="w-8 h-8 sm:w-10 sm:h-10"
											:style="{ color: getTechIcon(card.tech_name).color }"
											:stroke-width="1.75"
										/>
									</div>

									<div class="min-w-0">
										<h3 class="text-xl font-extrabold text-white mb-2 tracking-tight">
											{{ card.tech_name }}
										</h3>
										<p class="text-base text-slate-300 leading-relaxed text-pretty">
											{{ card.description }}
										</p>
									</div>
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
import { computed, ref, watch, type Component } from 'vue'
import { Palette, Code2 } from 'lucide-vue-next'
import {
	siHtml5,
	siBootstrap,
	siJavascript,
	siVuedotjs,
	siAxios,
	siNodedotjs,
	siGithub,
} from 'simple-icons'
import SegmentedNav, { type SegmentedNavItem } from '@/components/common/SegmentedNav.vue'
import { useCmsStore } from '@/stores/useCmsStore'

withDefaults(
	defineProps<{
		hideHeader?: boolean
	}>(),
	{
		hideHeader: false,
	},
)

const store = useCmsStore()

const FALLBACK_TAB = '核心必修'

// 依 CMS category_tab 動態分組，維持後台為唯一真實來源，前台不硬編碼任何分類清單
const groups = computed(() => {
	const ordered: { tab: string; cards: typeof store.techCards }[] = []
	for (const card of store.techCards) {
		const tab = card.category_tab || FALLBACK_TAB
		const existing = ordered.find((group) => group.tab === tab)
		if (existing) existing.cards.push(card)
		else ordered.push({ tab, cards: [card] })
	}
	return ordered
})

const active = ref(0)

// CMS 非同步載入或分類數量變動時，將選取索引夾回有效範圍，避免面板空白
watch(
	() => groups.value.length,
	(length) => {
		if (active.value > length - 1) active.value = 0
	},
)

const tabs = computed<SegmentedNavItem[]>(() =>
	groups.value.map((group) => ({
		key: group.tab,
		label: group.tab,
		badge: String(group.cards.length),
	})),
)

const activeGroup = computed(() => groups.value[active.value] ?? { tab: '', cards: [] })

const gridColumns = computed(() => {
	const count = activeGroup.value.cards.length
	if (count <= 1) return 'grid-cols-1 max-w-2xl mx-auto'
	if (count === 2) return 'grid-cols-1 md:grid-cols-2'
	return 'grid-cols-1 md:grid-cols-2 xl:grid-cols-3'
})

// 技術品牌圖示：優先使用 Simple Icons 官方 logo，無品牌圖示者退回 Lucide 通用圖示
// 深色底不可讀的品牌色（GitHub 近黑、Axios 深紫）以可讀色票覆寫
type TechIcon = { path?: string; component?: Component; color: string }

function brand(icon: { path: string; hex: string }, color?: string): TechIcon {
	return { path: icon.path, color: color || `#${icon.hex}` }
}

function getTechIcon(name: string): TechIcon {
	if (name.includes('HTML') || name.includes('CSS')) return brand(siHtml5)
	if (name.includes('Tailwind') || name.includes('Bootstrap')) return brand(siBootstrap)
	if (name.includes('Photoshop') || name.includes('Adobe') || name.includes('視覺'))
		return { component: Palette, color: '#31A8FF' }
	if (name.includes('JavaScript') || name.includes('ES6')) return brand(siJavascript)
	if (name.includes('Vue') || name.includes('Pinia')) return brand(siVuedotjs)
	if (name.includes('API') || name.includes('Axios')) return brand(siAxios, '#8B6CF0')
	if (name.includes('Node') || name.includes('MongoDB')) return brand(siNodedotjs)
	if (name.includes('Git') || name.includes('GitHub')) return brand(siGithub, '#E6EDF3')
	return { component: Code2, color: '#94A3B8' }
}
</script>

<style scoped>
.tech-fade-enter-active,
.tech-fade-leave-active {
	transition: opacity 0.24s ease-out, transform 0.24s ease-out;
}

.tech-fade-enter-from {
	opacity: 0;
	transform: translateY(10px);
}

.tech-fade-leave-to {
	opacity: 0;
	transform: translateY(-6px);
}

@media (prefers-reduced-motion: reduce) {
	.tech-fade-enter-active,
	.tech-fade-leave-active {
		transition: none;
	}
}
</style>
