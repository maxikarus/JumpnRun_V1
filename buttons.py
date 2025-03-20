import pygame


#CheckBox-Klasse
class CheckBox:
    def __init__(self, x, y, size=20, color=(0, 0, 0), check_color=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.check_color = check_color
        self.checked = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.checked:
            pygame.draw.line(screen, self.check_color, (self.rect.left + 4, self.rect.centery), (self.rect.centerx, self.rect.bottom - 4), 3)
            pygame.draw.line(screen, self.check_color, (self.rect.centerx, self.rect.bottom - 4), (self.rect.right - 4, self.rect.top + 4), 3)

#Normaler Button
class Button():
	def __init__(self, image, x_pos, y_pos, text_input, font):
		self.image = image
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_input = text_input
		self.text = font.render(self.text_input, True, "white")
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True

	def changeColor(self, position, font):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = font.render(self.text_input, True, "white")
		else:
			self.text = font.render(self.text_input, True, "#0a4635")  