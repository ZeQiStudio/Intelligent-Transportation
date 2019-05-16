/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/views/layout/Layout'

const tableRouter = {
  path: '/complex-table3',
  component: Layout,
  redirect: '/table/complex-table3',
  name: 'Table',
  meta: {
    title: 'Table',
    icon: 'nested'
  },
  children: [
    // {
    //   path: 'dynamic-table',
    //   component: () => import('@/views/table/dynamicTable/index'),
    //   name: 'DynamicTable',
    //   meta: {
    //     title: 'dynamicTable'
    //   }
    // },
    // {
    //   path: 'drag-table',
    //   component: () => import('@/views/table/dragTable'),
    //   name: 'DragTable',
    //   meta: { title: 'dragTable' }
    // },
    // {
    //   path: 'inline-edit-table',
    //   component: () => import('@/views/table/inlineEditTable'),
    //   name: 'InlineEditTable',
    //   meta: {
    //     title: 'inlineEditTable'
    //   }
    // },
    {
      path: 'complex-table3',
      component: () => import('@/views/table/complexTable3'),
      name: 'ComplexTable3',
      meta: {
        title: '道路违规行为'
      }
    }
  ]
}

export default tableRouter
