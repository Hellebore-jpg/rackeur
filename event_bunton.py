def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            # handle the left-button press in here
            self.label_click.setText("mousePressEvent LEFT")
        
        elif e.button() == Qt.MouseButton.MiddleButton:
            # handle the middle-button press in here.
            self.label_click.setText("mousePressEvent MIDDLE")
        
        elif e.button() == Qt.MouseButton.RightButton:
            # handle the right-button press in here.
            self.label_click.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label_click.setText("mouseReleaseEvent LEFT")
        
        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label_click.setText("mouseReleaseEvent MIDDLE")
        
        elif e.button() == Qt.MouseButton.RightButton:
            self.label_click.setText("mouseReleaseEvent RIGHT")
    
    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label_click.setText("mouseDoubleClickEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label_click.setText("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label_click.setText("mouseDoubleClickEvent RIGHT")