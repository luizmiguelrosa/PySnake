class Collision:
    def __init__(self, mask):
        self.mask = mask
        self.colliding = []

    def __getitem__(self, __value):
        for object in self.colliding:
            if object.collision_mask() == __value:
                return object
        return False


class Entity:
    def __init__(self, mask: str, x: float, y: float):
        self.x, self.y = x, y
        self.collision = Collision(mask)

    def collision_mask(self):
        return self.collision.mask

    def destroy(self):
        try:
            self.parent.delete_object(self.__hash__())
        except KeyError as e:
            print(e)

    def is_paused(self):
        return self.parent.paused


class Hud:
    def __init__(self, x: float, y: float, z_index: int):
        self.x, self.y, self.z_index = x, y, z_index

class Scene:
    def __init__(self, parent):
        self.parent = parent

    def create_object(self, name: str, object: Entity, mask: str, x: float, y: float, *args, **kwargs):
        return self.parent.objects.create_object(name, object, mask, x, y, *args, **kwargs)
    
    def delete_object(self, id):
        self.parent.objects.delete_object(id)

    def create_hud_object(self, name: str, object: Hud, x: float, y: float, z_index: int):
        return self.parent.hud.create_object(name, object, x, y, z_index)

    def object_exists(self, id):
        return self.parent.objects.object_exists(id)
    
    def get_objects_by_mask(self, mask: str):
        return self.parent.objects.get_objects_by_mask(mask)
    
    def get_total_objects_by_mask(self, mask: str):
        return self.parent.objects.get_total_objects_by_mask(mask)
    
    def colliding_with(self, object: Entity, _object: Entity):
        return self.parent.collisions.colliding_with(object, _object)