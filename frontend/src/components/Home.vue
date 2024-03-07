<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import axios from "axios";

let initd = false;
let modelInfo = ref([]);
let devicesInfo = ref({});

// items
const srcLangs = reactive([]);
const tgtLangs = reactive([]);

const srcLang = ref();
const tgtLang = ref();
const model = ref();
const device = ref();
const srctext = ref();
const tgtText = ref("訳文");
const honyakusiteiru = ref<string | boolean>();
const msg = ref();

// init page
const initQuery = async () => {
  let path = "/api/filter.fuck";
  if (initd) return undefined;
  await axios
    .post(path, {
      src: srcLang.value ? srcLang.value : null,
      tgt: tgtLang.value ? tgtLang.value : null,
      model: model.value ? model.value : null,
    })
    .then((response) => {
      modelInfo.value = response.data.info;
      langListRender();
    })
    .catch((error) => {
      console.log(error);
    });
  path = "/api/devices.fuck";
  if (initd) return undefined;
  await axios
    .get(path)
    .then((response) => {
      devicesInfo.value = response.data.devices;
    })
    .catch((error) => {
      console.log(error);
      msg.value = error.msg;
    });
};
const selectModel = () => {
  // model preload function, not avilable yet
};
// rend language selection
const langListRender = () => {
  const selectedModel = model.value;
  const filteredArr = modelInfo.value.filter(
    (value: any, index: any, array: string[]) => {
      return !(selectedModel && selectedModel != value.name);
    }
  );
  srcLangs.length = 0;
  tgtLangs.length = 0;
  for (let i = 0; i < modelInfo.value.length; i++) {
    if (!srcLangs.includes(modelInfo.value[i]["src"]))
      srcLangs.push(modelInfo.value[i]["src"]);
    if (!tgtLangs.includes(modelInfo.value[i]["tgt"]))
      tgtLangs.push(modelInfo.value[i]["tgt"]);
  }
};
// rend model selection filtes by languages
const modelListRender = computed((): string[] => {
  let filteredArr = modelInfo.value.filter(
    (value: any, index: any, array: string[]) => {
      return !(
        (srcLang.value && value.src != srcLang.value) ||
        (tgtLang.value && value.tgt != tgtLang.value)
      );
    }
  );
  let modelList: string[] = [];
  for (let i = 0; i < filteredArr.length; i++) {
    if (!modelList.includes((filteredArr[i] as any).name))
      modelList.push((filteredArr[i] as any).name);
  }
  if (!modelList.includes(model.value)) model.value = undefined;
  return modelList;
});
// rend device selection
const devices = computed((): string[] => {
  const deviceList = Object.keys(devicesInfo.value);
  return deviceList.length > 1 ? ["cpu", "gpu"] : ["cpu"];
});
// translation request
const honyaku = () => {
  if (!srctext.value || !srcLang.value || !tgtLang.value || !model.value) {
    tgtText.value = "訳文";
    return undefined;
  }
  const path = "/api/nmt.fuck";
  if (initd) return undefined;
  // honyakusiteiru.value = true;
  axios
    .post(path, {
      src: srcLang.value ? srcLang.value : null,
      tgt: tgtLang.value ? tgtLang.value : null,
      model: model.value ? model.value : null,
      text: srctext.value,
      device: device.value ? device.value : -1,
    })
    .then((response) => {
      tgtText.value = response.data.result;
      // honyakusiteiru.value = false;
    })
    .catch((error) => {
      console.log(error);
      msg.value = error.msg;
      honyakusiteiru.value = "error";
    });
};
//init
initQuery();
const refreshOptions = () => {
  srcLangs.length = 0;
  tgtLangs.length = 0;

  modelInfo.value = [];
  devicesInfo.value = {};

  srcLang.value = undefined;
  tgtLang.value = undefined;
  model.value = undefined;
  device.value = undefined;
  initd = false;
  initQuery();
};
</script>

<!-- :update:modelValue="modelListRender()" -->

<template>
  <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
    <!-- Main Content -->
    <v-container class="mb-6">
      <v-row no-gutters>
        <v-col cols="3">
          <v-select class="pa-2 ma-2 sl" base-color="#70a1ff" color="#1e90ff" label="原文の言語を選択" variant="outlined"
            no-data="nothing counld be selected" :items="srcLangs" v-model="srcLang"></v-select> </v-col><v-col
          cols="3">
          <v-select class="pa-2 ma-2 sl" base-color="#70a1ff" color="#1e90ff" label="訳文の言語を選択" variant="outlined"
            no-data="nothing counld be selected" :items="tgtLangs" v-model="tgtLang"></v-select>
        </v-col>
        <v-col cols="3">
          <v-select class="pa-2 ma-2 sl" label="NMTモデルを選択" base-color="#70a1ff" color="#1e90ff" variant="outlined"
            :items="modelListRender" v-model="model" :update:modelValue="selectModel()"></v-select>
        </v-col>
        <v-col cols="2">
          <v-select class="pa-2 ma-2 sl" label="設備を選択" base-color="#70a1ff" color="#1e90ff" variant="outlined"
            :items="devices" v-model="device"></v-select>
        </v-col>
        <v-col cols="auto" density="comfortable">
          <v-btn icon="mdi-cached" class="ma-5" color="#fd79a8" @click="refreshOptions()"></v-btn>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col :key="0">
          <v-sheet class="pa-2 ma-2 sl">
            <v-textarea label="翻訳するにはテキストを入力してください" variant="outlined" counter="512" base-color="#70a1ff"
              color="#1e90ff" :auto-grow="true" v-model="srctext" :loading="honyakusiteiru"
              :update:modelValue="honyaku()" :messages="msg"></v-textarea>
          </v-sheet>
        </v-col>
        <v-col :key="1">
          <v-sheet class="pa-2 ma-2">
            <v-textarea variant="solo-filled" bg-color="gray" base-color="#70a1ff" color="#1e90ff" :readonly="true"
              :flat="true" :auto-grow="true" v-model="tgtText"></v-textarea>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<style scoped>
/* .sl {
  color: #1e90ff;
} */
/* .src-text {
}
.tgt-text {
  border: none;
  background: gray;
} */
</style>
