"""Single canonical lesson order. Letters are sequence groups, not tool acronyms."""
GROUPS = (
    ('A', '第一组：从零开始，建立空间与操控基础', tuple(f'A{i:02}' for i in range(1, 9))),
    ('B', '第二组：把基础用成一个完整收集小游戏', tuple(f'B{i:02}' for i in range(1, 14))),
    ('C', '第三组：扩图、整合与首次交付', tuple(f'C{i:02}' for i in range(1, 13))),
    ('D', '第四组：按需要精修，再做最终验收', tuple(f'D{i:02}' for i in range(1, 8))),
    ('E', '第五组：有需求再学的专项', tuple(f'E{i:02}' for i in range(1, 8))),
)
ORDER = [ident for _, _, ids in GROUPS for ident in ids]
OPTIONAL = {f'D{i:02}' for i in range(1, 7)} | {f'E{i:02}' for i in range(1, 8)}
K_ONLY = 'E06'
GROUP_RESULTS = {
    'A': '能看懂对象与空间，借助AI完成走、跑、跳和固定/有限镜头观察。',
    'B': '静态资产进入同一庭院，完成十星拾取、反馈、重开与初级排错。',
    'C': '庭院连接林路和观景台，统一世界观感，整合角色、交互与一个目标平台。',
    'D': '选做资产精修或训练角；D07按已选范围完成整体验收。',
    'E': '只针对真正需要的导航、性能、效果或旋转问题选学；不阻塞小游戏交付。',
}


def route_label(ident):
    if ident == K_ONLY:
        return '选修｜全K，只理解用途'
    if ident.startswith('E'):
        return '专项选修｜满足前置后按需学'
    if ident in {'D05', 'D06'}:
        return '动作增强选修'
    if ident in {f'D{i:02}' for i in range(1, 5)}:
        return '美术强化选修'
    if ident == 'D07':
        return '主线收束｜只验已选范围'
    return '主线'


def next_unit(ident):
    """Default progression never silently enrolls a learner in an optional topic."""
    if ident not in ORDER:
        raise ValueError('Unknown canonical lesson: ' + ident)
    if ident == 'C12' or ident in {'D04', 'D06'}:
        return 'D07'
    if ident == 'D07' or ident.startswith('E'):
        return None
    index = ORDER.index(ident)
    return ORDER[index + 1] if index + 1 < len(ORDER) else None
