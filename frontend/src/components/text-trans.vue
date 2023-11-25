<template>
  <div class="text-trans">
    <div v-for="i in textFile.chunks" :key="i" class="text-trans__text-row">
      <div v-if="i.timestamp[0] < maxTime">
      </div>
      <div v-else>
        <div class="text-trans__text-colum">
          {{ getMaxedTimeText(this.maxTime) }}
        </div>
        <div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
/* eslint-disable */
import axios from "axios";

export default {
  name: "text-trans",
  data() {
    return {
      text: '',
      maxTime: 30
    }
  },
  props: {
    textFile: {
    },
  },
  computed: {
    getText() {
      let text = ''
      for (let i in this.textFile.chunks){
        text = text + this.textFile.chunks[i].text
        console.log(i)
    }
      return text
  },
  },
  methods: {
    getMaxedTimeText(time) {
      let min = time - time
      let maxTime = time
      let text = ''
      for (let i in this.textFile.chunks) {
        if (this.textFile.chunks[i].timestamp[0] < maxTime) {
          if (this.textFile.chunks[i].timestamp[0] >= min) {
            text = text + this.textFile.chunks[i].text
          }
        }
      }
      console.log('Max= ' + this.maxTime)
      console.log(text)
      return text
    }
  },
  updated() {
    console.log(1111)
    this.maxTime = this.maxTime + 30
  },
  created() {
    console.log('Создано')
  },
  beforeCreate() {

  }
}
</script>

<style lang="scss" scoped>
  .text-trans{
    display: flex;
    flex-direction: column;
    .text-trans__text-row {
      display: flex;
    }
  }
</style>