<script setup lang="ts">
import { useSidebarStore } from '@/store/sidebar';
import headers from "../commponents/header.vue"
import siderbar from "../commponents/sidebar.vue"

const sidebar = useSidebarStore();
</script>
<template>
	<headers/>
	<siderbar/>
	<div class="content-box" :class="{ 'content-collapse': sidebar.collapse }">
		<div class="content">
			<router-view>
			</router-view>
		</div>
	</div>
</template>

