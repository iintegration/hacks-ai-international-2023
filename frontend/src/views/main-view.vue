<template>
  <header-component @toggleMenu="toggleMenu" :menu-opened="isMenu" :selected-menu-item="menuSelectedItem">
  </header-component>
  <navigation-panel v-if="menuOpened"
                    :selectMenu="selectMenuItem"
                    :selected-button="selectedMenuItem"
                    :file-id="currentFileId"
                    @scroll.prevent
                    @wheel.prevent
                    @toggleMenu="toggleMenu" />
  <div class="main-view__body">
    <component :is="currentTab"
               class="component"
               :selectMenu="selectMenuItem"
               :selectFileId="selectFileId"
               :fileId="currentFileId"
    ></component>
  </div>
</template>

<script>
import headerComponent from "@/components/header-component";
import NavigationPanel from "@/components/navigation-panel";
import tabLections from "@/components/tab-lections";
import tabBase from "@/components/tab-base";
import tabFileview from "@/components/tab-fileview";
import tabSettings from "@/components/file-settings";
import tabTestfileview from "@/components/tab-testfileview";

export default {
  name: "main-view",
  data() {
    return {
      menuOpened: false,
      menuSelectedItem: '',
      currentFileId: {}
    }
  },
  components: {
    NavigationPanel,
    headerComponent,
    tabLections,
    tabBase,
    tabFileview,
    tabSettings,
    tabTestfileview
  },
  methods: {
    toggleMenu() {
      this.menuOpened = !this.menuOpened
      console.log(this.menuOpened)
    },
    selectMenuItem(item) {
      this.menuSelectedItem = item
      localStorage.menuItem = item
      console.log(item)
    },
    selectFileId(id){ // Занести id файла в кэш
      this.currentFileId = id
      localStorage.fileId = id
    }
  },
  computed: {
    isMenu(){
      return this.menuOpened
    },
    selectedMenuItem() {
      return this.menuSelectedItem
    },
    currentTab(){
      console.log("tab-" + this.menuSelectedItem.toLocaleLowerCase())
      return "tab-" + this.menuSelectedItem.toLocaleLowerCase()
    },
  },
  mounted() {
    //localStorage.menuItem = 'fileview' // Тестовые
    if (localStorage.menuItem) {
      this.menuSelectedItem = localStorage.menuItem
    }
    if (localStorage.fileId) {
      this.currentFileId = localStorage.fileId
    }
  },
  watch:{
    item(newItem)
    {
      localStorage.menuItem = newItem
    }
  }
}
</script>

<style lang="scss" scoped>
  .main-view__body {
    height: 80vh;
    min-width: 800px;
    display: flex;
    justify-content: center;
  }
</style>