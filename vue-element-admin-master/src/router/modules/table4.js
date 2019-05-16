/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/views/layout/Layout'

const tableRouter = {
  path: '/complex-table4',
  component: Layout,
  redirect: '/table/complex-table4',
  name: 'Table',
  meta: {
    title: 'Table',
    icon: 'guide'
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
      path: 'complex-table4',
      component: () => import('@/views/table/complexTable4'),
      name: 'ComplexTable4',
      meta: {
        title: '车辆跟踪'
      }
    }
  ]
}

export default tableRouter
