from engine.classes import Entity, Hud


class CollisionManager:
    def __init__(self, masks, object_manager):
        self.masks = masks
        self.object_manager = object_manager

    def in_mask_collision(self, object: Entity, other_object: Entity):
        return other_object.collision_mask() in self.masks[object.collision_mask()]

    def colliding_with(self, object: Entity, other_object: Entity):
        try:
            return self.in_mask_collision(object, other_object) and object.element.colliderect(other_object.element)
        except AttributeError:
            return False

    def get_collisions(self, object):
        collisions = []
        for other_object in self.object_manager.objects:
            if other_object != object and self.colliding_with(object, other_object):
                collisions.append(other_object)
        return collisions

    def update(self):
        for object in self.object_manager.objects:
            if object.collision.mask in self.masks:
                object.collision.colliding = self.get_collisions(object)


class Manager:
    def __init__(self, screen, parent):
        self.objects = []
        self.screen = screen
        self.parent = parent

    def update(self):
        for object in self.objects:
            object.update()

    def object_exists(self, id):
        return any(object.__hash__() == id for object in self.objects)

    def delete_all_objects(self):
        self.objects.clear()

    def delete_object(self, id):
        for i, object in enumerate(self.objects):
            if object.__hash__() == id:
                self.objects.pop(i)
                return
        raise KeyError("This object has not been instantiated")

    def get_total_objects(self):
        return len(self.objects)


class ObjectManager(Manager):
    def __init__(self, screen, parent):
        super().__init__(screen, parent)

    def create_object(self, name: str, object: Entity, mask: str, x: float, y: float, *args, **kwargs):
        other_object = object(mask, x, y, *args, **kwargs)
        other_object.name = name
        other_object.screen = self.screen
        other_object.parent = self.parent
        self.objects.append(other_object)
        return other_object
    
    def get_objects_by_mask(self, mask: str):
        return [object for object in self.objects if object.collision_mask() == mask]

    def get_total_objects_by_mask(self, mask: str):
        return sum(1 for object in self.objects if object.collision_mask() == mask)


class HudManager(Manager):
    def __init__(self, screen, parent):
        super().__init__(screen, parent)

    def sort(self):
        self.objects.sort(key=lambda o: o.z_index)

    def create_object(self, name: str, object: Hud, x: float, y: float, z_index: int):
        other_object = object(x, y, z_index)
        other_object.name = name
        other_object.screen = self.screen
        other_object.parent = self.parent
        self.objects.append(other_object)
        self.sort()
        return other_object