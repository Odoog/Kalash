<h1>Проект "auroRiffle"</h1>

<h2>Используемые модули:</h2>

<ul type="disk">
	<li>
		<h3> Разработка: </h3>
		<ul type="sycle">
			<li> 
				<p>
					<i> android: <br> &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp </i> python -> python-kivy-framework -> linux-virtual-box -> python-for-android -> buildozer -> adb -> .apk 
				</p>
			</li>
			<li> 
				<p>
					<i> ios: <br> &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp </i> python -> python-kivy-framework -> linux-virtual-box -> python-for-ios -> buildozer -> adb -> .ipa
				</p>
			</li>
		</ul>
	</li>
	<li>
		<h3> Тестирование: </h3>
		<ul type="sycle">
			<li>
				<p>
					<i> all platforms: <br> &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp </i> python -> python-kivy-framework -> linux-virtual-box -> linux-python-visual-tools
				</p>		
			</li>
		</ul>
	</li>
</ul>

<h2>Построение нейронной сети:</h2>

<p> В проекте используется рекурентная сверточная нейронная сеть, обученная на сетах <i> PASCAL VOC 2007, 2012, MS COCO </i> без сверточных слоёв. Сверточные слои были заменены
	на рекурентный классификатор с полносвязными слоями распределителями. </p>

<p> <i> Пример работы классификатора: </i> </p>

<img src="https://i.ibb.co/8YxSqd0/1.png">
<img src="https://i.ibb.co/VMD48gZ/2.png">
<img src="https://i.ibb.co/hYGCZ6s/3.png">
