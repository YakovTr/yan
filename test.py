# Connect combo box signals to sorting functions
self.classCombo.currentIndexChanged.connect(self.sortByClass)
self.lesson_nameCombo.currentIndexChanged.connect(self.sortByLesson)
self.dayCombo.currentIndexChanged.connect(self.sortByDay)
self.lesson_numCombo.currentIndexChanged.connect(self.sortByNumber)

self.classCombo = QComboBox(self)
self.cursor.execute("SELECT distinct class FROM high_school")
classes = [class_name[0] for class_name in self.cursor.fetchall()]
self.classCombo.addItems(classes)

self.lesson_nameCombo = QComboBox(self)
self.cursor.execute("SELECT distinct lesson_name FROM high_school")
names = [lesson_names[0] for lesson_names in self.cursor.fetchall()]
self.lesson_nameCombo.addItems(names)

self.dayCombo = QComboBox(self)
self.cursor.execute("SELECT distinct day FROM high_school")
day_name = [days[0] for days in self.cursor.fetchall()]
self.dayCombo.addItems(day_name)

self.lesson_numCombo = QComboBox(self)
self.cursor.execute("SELECT distinct lesson_num FROM high_school")
nums = [num[0] for num in self.cursor.fetchall()]
self.lesson_numCombo.addItems(nums)

combo_layout.addWidget(self.tablecombo)
combo_layout.addWidget(self.classCombo)
combo_layout.addWidget(self.lesson_nameCombo)
combo_layout.addWidget(self.dayCombo)
combo_layout.addWidget(self.lesson_numCombo)