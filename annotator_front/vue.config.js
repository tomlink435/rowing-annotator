const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,
  devServer:{
    host:'localhost',
    port:8094,
    proxy:{
      '/api':{
        target:'http://localhost:8000',
        changeOrigin:true,
        pathRewrite: {
          '/api':'',
          '^api':'api'
        }
      },

    }
  },
  productionSourceMap:true,
  chainWebpack:(config)=>{
    config.plugins.delete('prefetch');
  }
})
