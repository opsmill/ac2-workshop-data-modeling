import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    'readme',
    {
      type: 'category',
      label: 'Lab 1',
      link: { type: 'doc', id: 'lab1/readme' },
      items: [
        'lab1/setup',
        'lab1/start',
        'lab1/load_data',
        'lab1/explore',
        'lab1/modify',
        // 'lab1/summary',
      ],
    },
    {
      type: 'category',
      label: 'Lab 2',
      link: { type: 'doc', id: 'lab2/readme' },
      items: [
        'lab2/setup',
        'lab2/start',
        'lab2/load_data',
        'lab2/explore_schema',
        'lab2/explore_data',
        'lab2/explore_m2m_relationships'
        // 'lab2/summary',
      ],
    },
    {
      type: 'category',
      label: 'Lab 3',
      link: { type: 'doc', id: 'lab3/readme' },
      items: [
        'lab3/setup',
        'lab3/initialschema',
        'lab3/interfacerole',
        'lab3/interfacel2',
        // 'lab2/summary',
      ],
    },
  ]
};

export default sidebars;
