<template>
  <div  class="d1">
    <div id="pie-chart" style="width: 600px;height:400px;"></div>
    <div id="bar-chart" style="width: 600px;height:400px;"></div>
    <div id="word-cloud" style="width: 600px;height:400px;"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import * as echarts from 'echarts';
import 'echarts-wordcloud';

export default defineComponent({
  name: 'OlympicRowingStats',
  setup() {
    onMounted(() => {
      const pieChart = echarts.init(document.getElementById('pie-chart')!);
      const barChart = echarts.init(document.getElementById('bar-chart')!);
      const wordCloud = echarts.init(document.getElementById('word-cloud')!);

      const optionPie = {
        title: {
          text: '赛艇运动奥运金牌分布',
          subtext: '2023-2024',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
        },
        series: [
          {
            name: '金牌数',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 5, name: '美国' },
              { value: 3, name: '英国' },
              { value: 2, name: '德国' },
              { value: 4, name: '新西兰' },
              { value: 2, name: '澳大利亚' },
              { value: 1, name: '加拿大' },
              { value: 1, name: '丹麦' },
              { value: 1, name: '法国' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };

      const optionBar = {
        title: {
          text: '赛艇运动奥运金牌分布',
          subtext: '2023-2024',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: ['美国', '英国', '德国', '新西兰', '澳大利亚', '加拿大', '丹麦', '法国']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [5, 3, 2, 4, 2, 1, 1, 1],
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            }
          }
        ]
      };

      const optionWordCloud = {
        title: {
          text: '国际知名赛艇运动员',
          subtext: '2023-2024',
          left: 'center'
        },
        series: [{
          type: 'wordCloud',
      
          gridSize: 2,
          sizeRange: [12, 50],
          rotationRange: [-90, 90],
          shape: 'pentagon',
          width: 600,
          height: 400,
          drawOutOfBound: true,
          textStyle: {
            normal: {
              color: function () {
                return 'rgb(' + [
                  Math.round(Math.random() * 160),
                  Math.round(Math.random() * 160),
                  Math.round(Math.random() * 160)
                ].join(',') + ')';
              }
            }
          },
          data: [
            {name: 'Mahe Drysdale', value: 10000},
            {name: 'Eric Murray', value: 6181},
            {name: 'Hamish Bond', value: 4386},
            {name: 'Eric Murray', value: 4055},
            {name: 'Iztok Čop', value: 10000},
            {name: 'Olena Khyzhna', value: 6181},
            {name: 'Kim Crow', value: 4386},
            {name: 'Natalie Ross', value: 4055},
            {name: 'Caitlin Calkins', value: 10000},
            {name: 'Martin Sinković', value: 10000},
            {name: 'Valent Sinković', value: 6181},
            {name: 'Olaf Tufte', value: 4386},
            {name: 'Ekaterina Karsten', value: 4055},
            {name: 'Katherine Grainger ', value: 10000},
            {name: 'Heather Stanning', value: 6181},
            {name: 'Helen Glover', value: 4386},
            {name: 'Kim Brennan', value: 4055},
            {name: 'Xeno Müller', value: 10000},
            {name: 'Elisabeta Lipă', value: 4055},
            {name: 'Steve Redgrave ', value: 10000},
            {name: 'Matthew Pinsent', value: 6181},
            {name: 'Eleanor Logan', value: 4386},
            {name: 'Marnie McBean', value: 4055},
            {name: 'Kathrin Boron', value: 10000},
            // 更多运动员...
          ]
        }]
      };

      wordCloud.setOption(optionWordCloud);
      pieChart.setOption(optionPie);
      barChart.setOption(optionBar);
    });
  }
});
</script>
<style>
.d1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh; /* 根据需要调整 */
}
</style>


