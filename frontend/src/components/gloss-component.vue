<template>

  <div v-if="selectedTermi == glossTermin" style="background: #ff1d5e; border-radius: 10px; padding: 5px">
    <div style="display: flex;justify-content: space-between">
      <h1 @click="hightlightTermin(oneGloss.term)">
        {{oneGloss.term}}
      </h1>
      <div @click="deleteGlossTerm(oneGloss.term)">
        <img :src="require('@/assets/trashbin.png')" height="20" width="20" alt="1" style="cursor: pointer">
      </div>
    </div>
    <p>
      {{ oneGloss.definition }}
    </p>
  </div>
  <div v-else >
    <div style="display: flex; align-items: center; justify-content: space-between">
      <h1 @click="hightlightTermin(oneGloss.term)">
        {{oneGloss.term}}
      </h1>
      <div @click="deleteGlossTerm(oneGloss.term)">
        <img :src="require('@/assets/trashbin.png')" height="20" width="20" style="cursor: pointer">
      </div>
    </div>
    <p>
      {{ oneGloss.definition }}
    </p>
  </div>

</template>

<script>
export default {
  name: "gloss-component",
  data() {
    return {
      glossTermin: this.oneGloss.term
    }
  },
  props: {
    oneGloss: {
      type: Object
    },
    hightlightTermin: {
    },
    selectedTermi: {
    },
    deleteGlossTerm:{
    }
  },
  methods: {
  },
  beforeCreate() {
  }
}
</script>

<style lang="scss" scoped>
  h1 {
    cursor: pointer;
  }
</style>