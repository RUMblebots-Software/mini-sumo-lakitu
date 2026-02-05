super().__init__(
                root=img_dir,
                transform=transform,
                target_transform=target_transform,
                loader=loader,
                is_valid_file=is_valid_file
            )