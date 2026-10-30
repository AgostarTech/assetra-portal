import os

tag_path = "assets/models.py"
if os.path.exists(tag_path):
    with open(tag_path, "r", encoding="utf-8") as f:
        content = f.read()

    tag_model = """

class AssetTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='asset_tags')
    assets = models.ManyToManyField('Asset', related_name='custom_tags', blank=True)

    def __str__(self):
        return self.name
"""

    if "AssetTag" not in content:
        with open(tag_path, "a", encoding="utf-8") as f:
            f.write("\n" + tag_model)
        print("SUCCESS: AssetTag model added to assets/models.py!")
    else:
        print("NOTICE: AssetTag model already exists.")
