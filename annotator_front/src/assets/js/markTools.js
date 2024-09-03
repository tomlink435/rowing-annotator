/** @type {HTMLCanvasElement} */
var canvas = {};
var ctx = {};

function DrawImg() {
	// 鼠标是否移动
	this.moving = false;
	// 鼠标点击时的坐标
	this.dis = {};
	// 保存画布数据
	this.imgDataNow = "";
	// 保存上一步画布数据
	this.imgDataBack = "";
	// 矩形框坐标集合
	this.locations = [];
	// 当前绘画的矩形
	this.thisrect = {};
	// 画布初始大小
	this.width = 500;
	this.height = 500;
	// 图片地址
	this.imgUrl = "";
	// 指示当前图片是否可以进行标注，默认为false，即不可进行标注
	this.canAnnotate = false;

	const init = function(width, height, is_annotated) {
		canvas = document.querySelector("#canvas");
		// 获取画布上下文
		ctx = canvas.getContext("2d");
		// 调整画布大小
		canvas.width = width;
		canvas.height = height;
		this.eventBind();
	};
	this.eventBind = function() {
		//按下鼠标事件
		canvas.onmousedown = (ev) => {
			this.moving = true;
			//鼠标点击时的坐标
			this.dis = {
				x: ev.offsetX,
				y: ev.offsetY,
			};
		};

		//移动鼠标事件
		canvas.onmousemove = (ev) => {
			if (!this.moving) {
				return;
			}
			// this.drawLine(ev);
			if(this.canAnnotate){
				console.log("drawRect");
				this.drawRect(ev);
			}
			// this.drawRect(ev);
			
		};

		//松开鼠标事件
		canvas.onmouseup = (ev) => {
			this.moving = false;
			var rect = {
				// x: this.dis.x ,
				// y: this.dis.y ,
				x: this.dis.x < ev.offsetX ? this.dis.x : ev.offsetX,
				y: this.dis.y < ev.offsetY ? this.dis.y : ev.offsetY,
				width: Math.abs(ev.offsetX - this.dis.x),
				height: Math.abs(ev.offsetY - this.dis.y),
				// width: (ev.offsetX - this.dis.x),
				// height: (ev.offsetY - this.dis.y),
			};
			this.thisrect = rect;
			//将当前矩形坐标加入数组
			this.locations.push(rect);

			// 保存上一步画布数据
			this.imgDataBack = this.imgDataNow;
			//保存之前画布数据
			this.imgDataNow = ctx.getImageData(0, 0, canvas.width, canvas.height);
		};
	};
}

//通用功能
DrawImg.prototype.common = function() {
	//清除画布
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	//重新写入画布数据
	if (this.imgDataNow) {
		ctx.putImageData(this.imgDataNow, 0, 0);
	}
	//样式
	ctx.lineWidth = 2;
	ctx.strokeStyle = "red";
};

//撤销操作
DrawImg.prototype.cancel = function() {
	//清除画布
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	//重新写入画布数据
	if (this.imgDataBack) {
		ctx.putImageData(this.imgDataBack, 0, 0);
		this.imgDataNow = this.imgDataBack;
	} else {
		this.imgDataNow = this.imgDataBack;
	}
};

//画线
DrawImg.prototype.drawLine = function(ev) {
	// console.log("line");
	this.common();
	//画线
	ctx.beginPath();
	ctx.moveTo(this.dis.x, this.dis.y);
	ctx.lineTo(ev.offsetX, ev.offsetY);
	ctx.stroke();
};

// 鼠标画框
DrawImg.prototype.drawRect = function(ev) {
	// console.log("rect");
	this.common();
	//起始点
	var { x, y } = this.dis;
	// 终点
	// ev.offsetX, ev.offsetY
	// 长                      , 宽
	// Math.abs(ev.offsetX - x), Math.abs(ev.offsetY - y)

	ctx.beginPath();
	// ctx.rect(x, y, Math.abs(ev.offsetX - x), Math.abs(ev.offsetY - y)); //路径
	ctx.rect(x, y, (ev.offsetX - x), (ev.offsetY - y)); //路径

	ctx.stroke();
};

// 已有数据画框
DrawImg.prototype.dataDrawRect = function(x, y, width, height, tag_name) {
	// console.log("datarect");
	this.common()
	// 标注框样式
	ctx.lineWidth = 4;
	ctx.strokeStyle = "#00FF00";

	// 文字背景样式，画文字背景
	const text = tag_name;
	ctx.fillStyle = "#00FF00";
	ctx.font = "15px bolder 黑体";
	const fontwidth = ctx.measureText(text).width;
	ctx.fillRect(x, y, fontwidth + 3, 18);

	// 文字样式
	ctx.fillStyle = "#0000CD";
	ctx.textAlign = "left";
	ctx.textBaseline = "top";

	// 画标注框，画文字
	ctx.beginPath();
	ctx.rect(x, y, width, height); //路径
	ctx.stroke();
	ctx.fillText(text, x, y);

	this.imgDataNow = ctx.getImageData(0, 0, canvas.width, canvas.height);
};

DrawImg.prototype.selected = function(x, y, width, height, tag_name) {
	console.log("selected");
	// 选中框样式
	ctx.lineWidth = 4;
	ctx.strokeStyle = "#000080";

	// 文字背景样式，画文字背景
	const text = tag_name;
	ctx.fillStyle = "#000080";
	ctx.font = "15px bolder 黑体";
	const fontwidth = ctx.measureText(text).width;
	ctx.fillRect(x, y, fontwidth + 3, 18);

	// 文字样式
	ctx.fillStyle = "#F0F8FF";
	ctx.textAlign = "left";
	ctx.textBaseline = "top";

	// 画标注框，画文字
	ctx.beginPath();
	ctx.rect(x, y, width, height); //路径
	ctx.stroke();
	ctx.fillText(text, x, y);
}

//清除画布
DrawImg.prototype.clearCanvas = function() {
	//清除画布
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	this.imgDataNow = "";
	this.locations = [];
};

DrawImg.prototype.getDis = function(){
	return this.dis;
}

export { DrawImg };
