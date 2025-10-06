# neo4jRepository.py
import json
import uuid
from typing import List, Dict, Any, Optional

from neo4j import GraphDatabase, basic_auth

TNode = Dict[str, Any]
TArc = Dict[str, Any]

class Neo4jRepository:
    def __init__(self, uri: str, user: str, password: str, encrypted: bool = False):
        """
        Инициализация драйвера neo4j
        :param uri: например "bolt://localhost:7687"
        :param user: логин
        :param password: пароль
        :param encrypted: шифрованное соединение (TLS/SSL)
        """
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password), encrypted=encrypted)

    def close(self):
        """
        Закрытие драйвера
        """
        self.driver.close()

    # -----------------------
    # Вспомогательные функции
    # -----------------------
    @staticmethod
    def generate_random_string(length: int = 12) -> str:
        """Генерация случайной строки для URI (безопасная, читаемая)"""
        # Используем uuid4 для уникальности, обрезаем и делаем безопасную строку
        uid = uuid.uuid4().hex[:length]
        return f"node_{uid}"

    @staticmethod
    def transform_labels(labels: List[str], separator: str = ':') -> str:
        """Построить часть запроса с метками: `:Label1:Label2` (при пустом — пустая строка)"""
        if not labels:
            return ''
        safe = [f"`{l}`" for l in labels]
        return separator + separator.join(safe) if separator else ''.join(safe)

    @staticmethod
    def transform_props(props: Dict[str, Any]) -> str:
        """
        Преобразует dict свойств в Cypher map с экранированием.
        Использует json.dumps для безопасного представления значений.
        """
        if not props:
            return ''
        pairs = []
        for k, v in props.items():
            key = f'`{k}`'
            val = json.dumps(v, ensure_ascii=False)
            pairs.append(f"{key}: {val}")
        return "{" + ", ".join(pairs) + "}"

    # -----------------------
    # Сборщики (collect)
    # -----------------------
    @staticmethod
    def collect_node(record_node: Dict[str, Any]) -> TNode:
        """
        Преобразует результат neo4j node в TNode dict.
        Ожидается, что record_node — это dict с ключами: id, uri, title, description
        Если передан объект neo4j.Node, можно извлечь через .id и .items()
        """
        # Поддержка разных форматов входа
        if hasattr(record_node, "items") and 'uri' in record_node:
            # dict-like
            node = record_node
            return {
                "id": int(node.get("id")) if node.get("id") is not None else None,
                "uri": node.get("uri"),
                "title": node.get("title"),
                "description": node.get("description"),
                "arcs": node.get("arcs", []),
            }
        # Предполагаем, что это neo4j.Node
        try:
            props = dict(record_node.items())
            props['id'] = int(record_node.id)  # neo4j node id
            return {
                "id": props.get("id"),
                "uri": props.get("uri"),
                "title": props.get("title"),
                "description": props.get("description"),
                "arcs": props.get("arcs", []),
            }
        except Exception:
            # fallback: просто приведение в dict
            return dict(record_node)

    @staticmethod
    def collect_arc(rel) -> TArc:
        """
        Преобразует neo4j relationship или dict в TArc
        Ожидается: id, type (uri), startNode, endNode
        """
        if hasattr(rel, "type") and hasattr(rel, "id"):
            return {
                "id": int(rel.id),
                "uri": rel.type,
                "node_uri_from": rel.start_node.get("uri") if hasattr(rel, "start_node") else None,
                "node_uri_to": rel.end_node.get("uri") if hasattr(rel, "end_node") else None,
            }
        if isinstance(rel, dict):
            return {
                "id": int(rel.get("id")) if rel.get("id") is not None else None,
                "uri": rel.get("type") or rel.get("uri"),
                "node_uri_from": rel.get("node_uri_from"),
                "node_uri_to": rel.get("node_uri_to"),
            }
        # fallback
        return dict(rel)

    # -----------------------
    # CRUD: узлы
    # -----------------------
    def create_node(self, props: Dict[str, Any], labels: Optional[List[str]] = None) -> TNode:
        """
        Создать узел с указанными свойствами. Гарантированно добавляет uri, если не указан.
        Возвращает TNode.
        """
        labels = labels or []
        uri = props.get("uri") or self.generate_random_string()
        props_with_uri = {**props, "uri": uri}
        labels_part = f" {self.transform_labels(labels)}" if labels else ""
        props_part = self.transform_props(props_with_uri)

        cypher = f"CREATE (n{labels_part} {props_part}) RETURN n"
        with self.driver.session() as session:
            rec = session.run(cypher).single()
            node = rec["n"]
            node_props = dict(node.items())
            node_props["id"] = int(node.id)
            return self.collect_node(node_props)

    def get_all_nodes(self) -> List[TNode]:
        """Получить все узлы (без связей)"""
        cypher = "MATCH (n) RETURN n"
        with self.driver.session() as session:
            res = session.run(cypher)
            nodes = []
            for r in res:
                node = r["n"]
                props = dict(node.items())
                props["id"] = int(node.id)
                nodes.append(self.collect_node(props))
            return nodes

    def get_all_nodes_and_arcs(self) -> List[TNode]:
        """
        Получить все узлы и их связи (арки вложены в поле arcs для узла).
        Формируем список узлов, у каждого поле arcs = [TArc...]
        """
        cypher = """
        MATCH (a)-[r]->(b)
        RETURN a, r, b
        """
        with self.driver.session() as session:
            res = session.run(cypher)
            nodes_map: Dict[str, TNode] = {}
            for r in res:
                a = r["a"]
                b = r["b"]
                rel = r["r"]
                # собираем узлы
                a_props = dict(a.items()); a_props["id"] = int(a.id)
                b_props = dict(b.items()); b_props["id"] = int(b.id)
                a_node = self.collect_node(a_props)
                b_node = self.collect_node(b_props)
                # сохранить/обновить в map
                nodes_map[a_node["uri"]] = nodes_map.get(a_node["uri"], a_node)
                nodes_map[b_node["uri"]] = nodes_map.get(b_node["uri"], b_node)
                # собрать дугу
                arc = self.collect_arc(rel)
                # попытка получить node uri from/to из свойств rel (если есть)
                if not arc["node_uri_from"]:
                    arc["node_uri_from"] = a_node["uri"]
                if not arc["node_uri_to"]:
                    arc["node_uri_to"] = b_node["uri"]
                # добавить arc в узел-источник
                src = nodes_map[arc["node_uri_from"]]
                src.setdefault("arcs", []).append(arc)
            # также добавить отдельные изолированные узлы (без связей)
            # Получим все узлы и добавим те, которых нет в nodes_map
            all_nodes = self.get_all_nodes()
            for n in all_nodes:
                if n["uri"] not in nodes_map:
                    nodes_map[n["uri"]] = n
            return list(nodes_map.values())

    def get_nodes_by_labels(self, labels: List[str]) -> List[TNode]:
        """Выбрать узлы по меткам"""
        labels_part = self.transform_labels(labels)
        if labels_part:
            cypher = f"MATCH (n{labels_part}) RETURN n"
        else:
            cypher = "MATCH (n) RETURN n"
        with self.driver.session() as session:
            res = session.run(cypher)
            nodes = []
            for r in res:
                node = r["n"]
                props = dict(node.items())
                props["id"] = int(node.id)
                nodes.append(self.collect_node(props))
            return nodes

    def get_node_by_uri(self, uri: str) -> Optional[TNode]:
        cypher = "MATCH (n {`uri`: $uri}) RETURN n LIMIT 1"
        with self.driver.session() as session:
            rec = session.run(cypher, uri=uri).single()
            if not rec:
                return None
            node = rec["n"]
            props = dict(node.items()); props["id"] = int(node.id)
            return self.collect_node(props)

    def update_node(self, uri: str, props: Dict[str, Any]) -> Optional[TNode]:
        """
        Обновляет свойства узла с указанным uri (замена/дополнение).
        Возвращает обновлённый узел.
        """
        # формируем SET n += { ... } используя параметры
        param_map = {f"p_{k}": v for k, v in props.items()}
        set_parts = ", ".join([f"n.`{k}` = $p_{k}" for k in props.keys()])
        cypher = f"MATCH (n {{`uri`: $uri}}) SET {set_parts} RETURN n"
        params = {"uri": uri}
        params.update(param_map)
        with self.driver.session() as session:
            rec = session.run(cypher, **params).single()
            if not rec:
                return None
            node = rec["n"]
            p = dict(node.items()); p["id"] = int(node.id)
            return self.collect_node(p)

    def delete_node_by_uri(self, uri: str) -> bool:
        """
        Удаляет узел по uri. Удаляет также все связанные арки.
        Возвращает True если был удалён хотя бы один узел.
        """
        cypher = "MATCH (n {`uri`: $uri}) DETACH DELETE n RETURN COUNT(n) as cnt"
        with self.driver.session() as session:
            rec = session.run(cypher, uri=uri).single()
            cnt = rec["cnt"] if rec else 0
            return int(cnt) > 0

    # -----------------------
    # CRUD: дуги (арки)
    # -----------------------
    def create_arc(self, node1_uri: str, node2_uri: str, rel_type: str = "RELATED", props: Optional[Dict[str, Any]] = None) -> Optional[TArc]:
        """
        Создать арку между двумя узлами по uri (если узлы не найдены — операция завершится без создания).
        Возвращает TArc или None.
        """
        props = props or {}
        props_part = self.transform_props(props)
        cypher = f"""
        MATCH (a {{`uri`: $uri1}}), (b {{`uri`: $uri2}})
        CREATE (a)-[r:`{rel_type}` {props_part}]->(b)
        RETURN r, a, b
        """
        with self.driver.session() as session:
            rec = session.run(cypher, uri1=node1_uri, uri2=node2_uri).single()
            if not rec:
                return None
            rel = rec["r"]
            arc = self.collect_arc(rel)
            # попытка извлечь node uri из узлов в ответе
            a = rec.get("a"); b = rec.get("b")
            if a and b:
                arc["node_uri_from"] = a.get("uri") if hasattr(a, "get") else (a["uri"] if "uri" in a else None)
                arc["node_uri_to"] = b.get("uri") if hasattr(b, "get") else (b["uri"] if "uri" in b else None)
            return arc

    def delete_arc_by_id(self, arc_id: int) -> bool:
        """
        Удалить арку по внутреннему id relationship. Возвращает True если удалено.
        """
        cypher = "MATCH ()-[r]-() WHERE id(r) = $rid DELETE r RETURN COUNT(r) as cnt"
        with self.driver.session() as session:
            rec = session.run(cypher, rid=arc_id).single()
            cnt = rec["cnt"] if rec else 0
            return int(cnt) > 0

    # -----------------------
    # Утилиты
    # -----------------------
    def run_custom_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Выполнить произвольный Cypher query и вернуть список строк (каждая — dict)
        """
        params = params or {}
        with self.driver.session() as session:
            res = session.run(query, **params)
            out = []
            for r in res:
                # преобразуем Record в dict
                out.append({k: (v if not hasattr(v, "items") else dict(v.items())) for k, v in dict(r).items()})
            return out
